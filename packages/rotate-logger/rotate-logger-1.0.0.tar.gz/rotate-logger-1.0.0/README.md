# Python Rotate Native Logger
***
|Maintainer||
| ------------- |:-------------:| 
| email      | andriyunantoreza@gmail.com |

### Requirement:
- Python 3.xx

### How it work?
1. Initialize once this function
    ```
    native_logger.configure_rotating_logger('generator')
    ```

    |Param|.|.| Default value |
    | ------------- |:-------------| :------------- | :------------- |
    | logger_name      | mandatory | name of logger, so you can access it from anywhere with specific logger name ||
    | debug      | optional | debug used for debugging purpose, if you want write logger.info on file, you can enable debug | False |
    | backup_count      | optional | how many backup count that you want | 14 |
    | hour      | optional | hour (0-23) when log change to next file rotate | 3 |
    | interval      | optional | interval day you want to backup | 1 |

2. Use everywhere
    
    Remember name of logger that you initialize, in this case I initialize using name **generator** and get the logger
    ```
    generator_logger = logging.getLogger('generator')
    generator_logger.warning('This is warning logger')
    ```

3. Check your log in log folder
    
    Note: 
        
        1. Make sure you have permission to create folder log
        2. debug.info is not write on file, set debug to True if you want it
        3. Have fun!
        
   
  