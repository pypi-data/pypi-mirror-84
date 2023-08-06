#!/usr/bin/env python
# coding: utf-8

# # EC Errors

# In[11]:


class EcError( Exception ):
    """
    Represents an EC Error.
    """
    
    errors = {
        # errors with value as key and ( code, message ) as value.
        -1: ( 
            'ERR_GEN_NOTCONNECTED', 
            'No instrument connected.' 
        ),
        
        -9: (
            'ERR_GEN_ECLAB_LOADED',
            'ECLab firmware laoded on instrument.'
        ),
        
        -11: ( 
            'ERR_GEN_USBLIBRARYERROR', 
            'USB library not loaded in memory.' 
        ),
        
        -200: (
            'ERR_COMM_COMMFAILED',
            'Communication with the instrument failed.'
        ),
        
        -201: (
            'ERR_COMM_CONNECTIONFAILED',
            'Could not establish communication with instrument.'
        ),
        
        -204: (
            'ERR_COMM_ALLOCMEMFAILED',
            'Cannot allocate memory in the instrument.'
        ),
        
        -308: (
            'ERR_FIRM_FIRMWARENOTLOADED',
            'No firmware loaded on channel.'
        ),
        
        -400: (
            'ERR_TECH_ECCFILENOTEXISTS',
            'ECC file does not exist.'
        ),
        
        -401: (
            'ERR_TECH_INCOMPATIBLEECC',
            'Ecc file not compatible with the channel firmware.'
        )
    }
    
    
    def __init__( self, value = None, code = None, message = None ):
        """
        Creates an EcError. 
        If value is passed code and message are automatically filled if found,
        but overridden if also passed.
        
        :param value: The value of the error. [Default: None]
        :param code: The error code. [Default: None]
        :param message: The error message.
        :returns: EcError
        """
        if value is not None:
            try:
                ( code, message ) = EcError.errors[ value ]

            except KeyError as err:
                raise ValueError( 'Unknown error value {}.'.format( value ) )
        
            out = '{code} ({value}): {message}'.format( 
                value = value,
                code = code,
                message = message
            )
            
        else:
            # no error value
            out = ''
        
        super( EcError, self ).__init__( out )


# In[ ]:





# # Work
