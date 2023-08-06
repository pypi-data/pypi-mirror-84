#!/usr/bin/env python
# coding: utf-8

# # Biologic Device
# Library for connecting to and controlling a Biologic device.

# # API

# In[1]:


import logging
import ctypes as c
import platform
from collections import namedtuple

from .lib.ec_errors import EcError
from .lib import ec_find as ecf
from .lib import ec_lib  as ecl


# # Biologic Device

# In[ ]:


TechParams = namedtuple( 'TechParams', [
    'technique',
    'parameters'
] )

TechData = namedtuple( 'TechData', [
    'data',
    'info',
    'values'
] )


# In[3]:


class BiologicDevice:
    """
    Represents a Biologic Device
    """
    
    def __init__( 
        self,
        address,
        timeout = 5
    ):
        """
        :param address: The address of the device to connect to.
        :param timeout: Timeout in seconds. [Defualt: 5]
        """
        self.__address = address
        self.timeout = timeout
        
        self.__init_variables()
        
        
    def __del__( self ):
        if self.is_connected():
            self.disconnect()
    
    #--- properties ---
    
    @property
    def address( self ):
        """
        :returns: Connection string of device.
        """
        return self.__address
    
    
    @property
    def idn( self ):
        """
        :returns: Device identifier.
        """
        return self.__idn
    
    
    @property
    def kind( self ):
        """
        :returns: Device model.
        :raises: RuntimeError if no device is connected at the connection string.
        """
        devs = ecf.find_devices()
        for device in devs:
            if self.address == device.connection_string:
                return device.kind
            
        raise RuntimeError( 'No device found at {}.'.format( self.address ) )
    
    
    @property
    def info( self ):
        """
        :returns: DeviceInfo object.
        """
        return self.__info
    
    
    @property
    def plugged( self ):
        """
        :returns: List of channel availablilities.
        """
        return self.__plugged
    
    
    @property
    def channels( self ):
        """
        :returns: List of ChannelInfo objects.
        """
        if not self.is_connected():
            # device not connected
            raise EcError( -1 ) 
        
        return [ 
            ecl.channel_info( self.idn, ch ) if available else None
            for ch, available in enumerate( self.plugged )
        ]     
    
    @property
    def techniques( self ):
        """
        :returns: List of TechParams loaded on each channel.
        """
        return self.__techniques
    
    #--- methods ---
    
    
    def connect( self, bin_file = None, xlx_file = None ):
        """
        Connects to the device at the address. Checks channel status.
        
        :param bin_file: Path to the bin file to use. If None, uses default.
            [Default: None]
        :param xlx_file: Path to the xilinx file to use. If None, uses default.
            [Default: None]
        """
        if self.idn is not None:
            raise RuntimeError( 'Device already connected.' )
        
        ( idn, info ) = ecl.connect( self.address, self.timeout )
        
        self.__idn = idn
        self.__info = info
        
        # initialize channels
        chs = list( range( self.info.NumberOfChannels ) )
        
        try:
            ecl.init_channels( 
                self.idn, chs, bin_file = bin_file, xlx_file = xlx_file 
            )
            
        except EcError as err:
            if err.value is -9:
                # ECLab firmware loaded
                pass
        
        # get channel info
        self.__plugged = ecl.get_channels( 
            self.idn, 
            self.info.NumberOfChannels 
        ) 
        
        self.__techniques = [ list() for ch in self.plugged ]
    
        
    def disconnect( self ):
        """
        Disconnect form the device.
        """
        if self.idn is None:
            raise RuntimeError( 'Device is not connected.' )
        
        ecl.disconnect( self.idn )
        
        self.__init_variables() # reset vairables
        
        
    def is_connected( self ):
        """
        Returns if the device is conencted or not.
        
        :returns: Boolean descirbing the state of connection.
        """
        if self.idn is None:
            return False
        
        return ecl.is_connected( self.idn )
        
        
    def load_technique( 
        self, 
        ch, 
        technique, 
        params, 
        index = 0, 
        last = True,
        types = None
    ):
        """
        Loads a single technique on to the given channel.
        
        :param ch: The channel to load the technique on to.
        :param technique: Name of the technique to load.
        :param params: A dictionary of parameters to use.
        :param index: Index of the technique. [Default: 0]
        :param last: Whether this is the last technique. [Default: True]
        :param types: List of dictonaries or Enums from technique_fields 
            to cast parameters, or None if no casting is desired. 
            [Default: None]
        """
        if self.idn is None:
            # not connected
            raise RuntimeError( 'Device not connected.')
        
        first = ( index is 0 )
        
        if types is not None:
            params = ecl.cast_parameters( params, types )
            
        ecc_params = ecl.create_parameters( params, index )
        technique = ecl.technique_file( technique, self.kind )
        
        ecl.load_technique( 
            self.idn, ch, technique, ecc_params, first, last 
        )
        
        # update technques
        self.__techniques[ ch ].insert( 
            index, TechParams( technique, params )
        )
    
    
    def load_techniques( self, ch, techniques, parameters, types = None ):
        """
        Loads a series of techniques on to the given channel.
        
        :param ch: Channel.
        :param techniques: A list of techniques.
        :param parameters: A list of dictionaries of key: value parameters,
            to use for the corresponding technique.
        :param types: List of dictonaries or Enums from technique_fields 
            to cast parameters, or None if no casting is desired. 
            [Default: None]
        """
        for index, technique in enumerate( techniques ):
            params = parameters[ index ]
            last = ( index == len( techniques ) - 1 )
            
            if isinstance( types, list ):
                kinds = types[ index ]
                
            elif types is None:
                kinds = None
                
            else:
                raise TypeError( 'Invalid types provided.')
                
            self.load_technique( ch, tech, params, index, last, kinds )
    
    
    def update_parameters( 
        self, 
        ch, 
        technique, 
        parameters, 
        index = 0, 
        types = None 
    ):
        """
        Updates technique parameters.
        
        :param ch: Channel.
        :param technique: Name of the technique.
        :param parameters: Dictionary of new parameter-values.
        :param index: Index of the technique. [Default: 0]
        :param types: Dictonary or Enum from technique_fields 
            to cast parameters, or None if no casting is desired. 
            [Default: None]
        """
        ecc_params = ecl.create_parameters( parameters, index, types )
        
        ecl.update_parameters( 
            self.idn, ch, technique, ecc_params, index, self.kind 
        )
        
        # update techniques
        self.__techniques[ ch ][ index ] = TechParams( technique, parameters )
    
    
    def start_channel( self, ch ):
        """
        Starts a device channel.
        
        :param ch: Channel to start.
        """
        ecl.start_channel( self.idn, ch )
    
    
    def start_channels( self, chs = None ):
        """
        Starts multiple channels.
        
        :param chs: List of channels to start, or None to start all.
            [Default: None]
        """
        if chs is None:
            # start all channels
            chs = list( range( self.info.NumberOfChannels ) )
        
        ecl.start_channels( self.idn, chs )
        
    
    def stop_channel( self, ch ):
        """
        Stops a device channel.
        
        :param ch: Channel to stop.
        """
        ecl.stop_channel( self.idn, ch )
    
    
    def stop_channels( self, chs = None ):
        """
        Stops multiple channels.
        
        :param chs: List of channels to stop, or None to stop all.
            [Default: None]
        """
        if chs is None:
            # stop all channels
            chs = list( range( self.info.NumberOfChannels ) )
        
        ecl.stop_channels( self.idn, chs )
    
    
    def channel_info( self, ch ):
        """
        Gets channel info.
        
        :param ch: The channel to probe.
        :returns: Chanenl info.
        """
        info = ecl.channel_info( self.idn, ch )
        
        return info
    
    
    def get_values( self, ch ):
        """
        Gets the current data on the channel.
        
        :param ch: Channel.
        :returns: A dictionary of key-value pairs.
        """
        values = ecl.get_values( self.idn, ch )
        
        return values
        
    
    def get_data( self, ch ):
        """
        Gets data stored on the channel.
        
        :param ch: Channel.
        :returns: TechData object with properties [ data, info, value ].
        """  
        
        ( data, info, values ) = ecl.get_data( self.idn, ch )
        return TechData( data, info, values )
    
        
    
    #--- private methods ---
        
    def __init_variables( self ):
        """
        Initializes instance variables.
        """
        self.__idn        = None # device identifier
        self.__info       = None # device info
        self.__plugged    = None # list of plugged in channels
        self.__techniques = None #list of channel techniques


# # Work

# In[ ]:




