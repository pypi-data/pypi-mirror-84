
"""
Fancy terminal logging.

Useful for tracking performance of machine learning
models by tracking some parameters to terminal.

Author: Nishant Prabhu
"""

import termcolor
from termcolor import cprint


class TerminalLogger:

    """
    Functionality for logging to terminal.

    Args:
        float_precision <int>
            Precision of float type variables that should
            be displayed. Defaults to 4. This can be overriden
            for each variable separately in the 'log' method.

    Returns:
        TerminalLogger object. 
    
    """

    def __init__(self, float_precision=4):
        
        self.float_precision = float_precision
    

    def epoch_marker(self, epoch, total_epochs=None, color='green', caps=True):
        """
        A quirky marker for the current epoch.

        Args:
            epoch <int>
                The current epoch number.
            total_epochs <int> (optional)
                Total number of epochs.
            color <str> (optional)
                Valid terminal color string. Defaults to 'green'
            caps <bool> (optional)
                Whether the text will be all caps or not. Defaults to True.

        Returns:print line
        """
        if isinstance(total_epochs, int):
            if caps:
                cprint("\nEPOCH {}/{}".format(epoch, total_epochs), color=color)
                cprint("---------------------------------------------------------", color=color)
            else:
                cprint("\nEpoch {}/{}".format(epoch, total_epochs), color=color)
                cprint("---------------------------------------------------------", color=color)
        
        else: # For any case where total_epochs is not an integer
            if caps:
                cprint("\nEPOCH {}".format(epoch), color=color)
                cprint("---------------------------------------------------------", color=color)
            else:
                cprint("\nEpoch {}".format(epoch), color=color)
                cprint("---------------------------------------------------------", color=color)


    def log(self, param_dict):
        """
        Define the parameters that must be tracked for logging.

        Args:
            param_dict <dict>
                Dictionary of values to be logged in the example 
                format below.

                param_dict = {
                    'Batch': 1,
                    'Some random number': 0.89435,
                    'Squared error': {'value': 0.33253454, 'precision': 4}
                }
            
                For data types like int and str, or if no other arguments are 
                required, the user may pass the value of the variable as the value 
                of that key. Precision will be processed only for float type 
                parameters. If no precision is specified, it defaults to 
                float_precision specified at initialization.

        Returns:
            Nothing. 

        """
        strings = []
        def_prec = '{{:.{}f}}'.format(self.float_precision)

        for i, (k, v) in enumerate(param_dict.items()):
            
            if i == len(param_dict)-1:
                
                if isinstance(v, dict):
                    if not 'value' in v.keys():
                        raise ValueError("Please pass the value of {} with the 'value' key".format(k))

                    if isinstance(v['value'], float):
                        if 'precision' in v.keys():
                            fmt = '{{:.{}f}}'.format(v['precision'])
                            strings.append("[{}] {}".format(k, fmt).format(v['value']))
                        else:
                            strings.append("[{}] {}".format(k, def_prec).format(v['value']))
                    
                    else:
                        strings.append("[{}] {}".format(k, v['value']))
                
                elif isinstance(v, float):
                    strings.append("[{}] {}".format(k, def_prec).format(v))

                else:
                    strings.append("[{}] {}".format(k, v))

            else:
                if isinstance(v, dict):
                    if not 'value' in v.keys():
                        raise ValueError("Please pass the value of {} with the 'value' key".format(k))

                    if isinstance(v['value'], float):
                        if 'precision' in v.keys():
                            fmt = '{{:.{}f}}'.format(v['precision'])
                            strings.append("[{}] {} -".format(k, fmt).format(v['value']))
                        else:
                            strings.append("[{}] {} -".format(k, def_prec).format(v['value']))
                    
                    else:
                        strings.append("[{}] {} -".format(k, v['value']))
                
                elif isinstance(v, float):
                    strings.append("[{}] {} -".format(k, def_prec).format(v))

                else:
                    strings.append("[{}] {} -".format(k, v))

        full_string = " ".join(strings)
        print(full_string)