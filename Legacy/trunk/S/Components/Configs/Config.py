## @ingroup Components-Configs
# Config.py
#
# Created:  Oct 2014, T. Lukacyzk
# Modified: Jan 2016, T. MacDonald

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

from Legacy.trunk.S.Core    import Diffed_Data
from Legacy.trunk.S.Vehicle import Vehicle

# ----------------------------------------------------------------------
#  Config
# ----------------------------------------------------------------------

## @ingroup Components-Configs
class Config(Diffed_Data,Vehicle):
    """ SUAVE.Components.Config()
    
        The Top Level Configuration Class
        
            Assumptions:
            None
            
            Source:
            N/A
    """
    
    def __defaults__(self):
        """ This sets the default values for the configuration.
        
                Assumptions:
                None
                
                Source:
                N/A
                
                Inputs:
                None
                
                Outputs:
                None
                
                Properties Used:
                N/A
        """
        self.tag    = 'config'
        self._base  = Vehicle()
        self._diff  = Vehicle()
