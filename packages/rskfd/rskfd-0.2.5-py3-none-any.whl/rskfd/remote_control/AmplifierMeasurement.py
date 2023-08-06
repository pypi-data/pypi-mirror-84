# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 13:31:30 2019

@author: RAMIAN
"""

from rskfd import InstrumentError

class AmplifierMeasurement(object):
    __ChannelName = None
    __Handle = None
    __Persistence = None
    
    def __init__(self, instrumentHandle, ChannelName="Amplifier", Overwrite = True, Persistence = True,
                 CenterFrequency = 1e9):
        self.__ChannelName = ChannelName
        self.__Handle = instrumentHandle
        self.__Persistence = Persistence
        
        #Check if channel already exists
        channellist = self.__Handle.Query( "INST:LIST?")
        if channellist.find(self.__ChannelName ) != -1:
            if Overwrite:
                self.__Handle.Write( "INST:DEL "+self.__ChannelName)
            else:
                raise InstrumentError("Channel "+self.__ChannelName+" already exists!")
        
        self.__Handle.Write( "INST:CRE AMPL,'" +self.__ChannelName+"'")
        self.__Handle.ChannelSelect( self.__ChannelName)
        
        self.__Handle.Write( "INIT:CONT OFF")
        self.__Handle.Write( "FREQ:CENT " + str(CenterFrequency))


    def __del__( self):
        if self.__Persistence == False:
            self.__Handle.Write( "INST:DEL "+self.__ChannelName)



    def AllCOmpensationsOff( self):
        self.__Handle.ChannelSelect( self.__ChannelName)
        
        self.__Handle.Write( "CONF:SIGN:ERR:EST:IQIM:STAT OFF")
        self.__Handle.Write( "CONF:SIGN:ERR:EST:ADR:STAT OFF")
        self.__Handle.Write( "CONF:SIGN:ERR:EST:SRAT:STAT OFF")
        

    def QueryAllSettings( self):
        self.__Handle.ChannelSelect( self.__ChannelName)
        self.__Handle.Query( "CONF:SETT;*OPC?")
        
    def QueryWaveform( self):
        import time
        
        self.__Handle.ChannelSelect( self.__ChannelName)
        self.__Handle.Write("CONF:REFS:CGW:READ")
        ledstate = self.__Handle.Query("CONF:REFS:CGW:LEDS?")
        loopcount = 0
        while (ledstate.find("GRE") != 0) & (loopcount < 5):
            time.sleep(.5)
            ledstate = self.__Handle.Query("CONF:REFS:CGW:LEDS?")
            loopcount += 1
        if ledstate.find("GRE") != 0:
            raise InstrumentError("Failed to load waveform!")
        

    def ConnectGenerator( self, GeneratorIp, QueryAll = True, QueryWv = True, DetachFrequency = False):
        import time
        
        self.__Handle.ChannelSelect( self.__ChannelName)
        if DetachFrequency:
            self.__Handle.Write("CONF:GEN:FREQ:CENT:SYNC:STAT OFF")
        
        #COnnect and query 2x
        self.__Handle.Write( "CONF:GEN:IPC:ADDR '" + GeneratorIp + "'")
        connstate = self.__Handle.Query( "CONF:GEN:CONN:CST?")
        loopcount = 0
        while (connstate.find("NCON") == 0) & (loopcount < 5):
            time.sleep(.2)
            connstate = self.__Handle.Query( "CONF:GEN:CONN:CST?")
            loopcount += 1
        if connstate.find("NCON") == 0:
            raise InstrumentError("Cannot connect to "+GeneratorIp+"!")
        
        time.sleep(.5)
        if QueryAll:
            self.QueryAllSettings( )
          
        time.sleep(.5)
        if QueryWv:
            self.QueryWaveform()
            
            
                
    def DoDirectDpd( self, NumberOfDPDSteps = 5, NumberOfIQAverages = 10):
        
        self.__Handle.ChannelSelect( self.__ChannelName)
        
        if "K18D" in self.__Handle.GetOpt():
            self.__Handle.ChannelSelect( self.__ChannelName)
            if( NumberOfIQAverages == 0):
                self.__Handle.Write( "SWE:IQAV:STAT OFF")
            else:
                self.__Handle.Write( "SWE:IQAV:STAT ON")
                self.__Handle.Write( "SWE:IQAV:COUN "+str(NumberOfIQAverages))
                
            self.__Handle.Write( "CONF:DDPD:STAT ON")
            self.__Handle.Write( "CONF:DDPD:COUN "+str(NumberOfDPDSteps))
            self.__Handle.Query( "CONF:DDPD:STAR;*OPC?")
            # Switch off Averaging after DPD
            self.__Handle.Write( "SWE:IQAV:STAT OFF")
                
        else:
            raise InstrumentError("K18D not available!")
            
    def SetDpd( self, State):
        
        self.__Handle.ChannelSelect( self.__ChannelName)
        
        if State:
            helper = "ON"
        else:
            helper = "OFF"
        self.__Handle.Query( "CONF:DDPD:STATE "+helper+";*OPC?")

        

    def MeasureAmplifier( self):
        self.__Handle.ChannelSelect( self.__ChannelName)
        self.__Handle.Query( "INIT:IMM;*OPC?")
    
        return 1


    def SetupK18ForFile( self, reffile, measfile, DoAnalysis=True):
        import os

        self.__Handle.ChannelSelect( self.__ChannelName)
        self.__Handle.Write( 'INIT:CONT OFF')
        if( DoAnalysis==False):
            self.__Handle.Write( "SENS:SWE:LENG 3")
        self.__Handle.Write( 'CONF:GEN:CONT OFF')
        self.__Handle.Write( 'CONF:REFS:CWF:FPAT \'' + reffile + '\'')
         # This can take a little longer
        timeout = self.__Handle.GetTimeout()
        self.__Handle.SetTimeout( None)
        self.__Handle.Query( 'CONF:REFS:CWF:WRIT;*OPC?')
        self.__Handle.SetTimeout( timeout)
        self.__Handle.Write( 'CONF:SYNC:DOM IQD')
        self.__Handle.Write( 'CONF:SYNC:CONF 65')
        self.__Handle.Write( 'LAY:REPL:WIND \'3\',MRES')
        self.__Handle.Write( 'LAY:REPL:WIND \'5\',PRES')
        self.__Handle.Query( 'LAY:ADD? \'5\',BEL,RFSP')
        self.__Handle.Query( 'LAY:ADD? \'7\',RIGH,SEVM')
        self.__Handle.Write( 'INP:FILE:PATH \'' + measfile + '\'')
        self.__Handle.Write( 'INP:SEL FIQ')
    
        self.__Handle.Query( '*OPC?')

    