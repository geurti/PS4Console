### 
#
# Console completer based on Doug Hellmann's PyMOTW writeup on readline.
# https://doughellmann.com/blog/2008/11/30/pymotw-readline/ 
#
#

import readline
import logging

#LOG_FILENAME = '/tmp/completer.log'
#logging.basicConfig(filename=LOG_FILENAME,
#                    level=logging.DEBUG,
#                    )

class CommandCompleter(object):
    
    def __init__(self, options,validModuleNames):
        self.options = options
        self.validModuleNames = validModuleNames
        self.current_candidates = []
        return

    def complete(self, text, state):
        response = None
        if state == 0:
            # This is the first time for this text, so build a match list.
            
            origline = readline.get_line_buffer()
            begin = readline.get_begidx()
            end = readline.get_endidx()
            being_completed = origline[begin:end]
            words = origline.split()

            logging.debug('origline=%s', repr(origline))
            logging.debug('begin=%s', begin)
            logging.debug('end=%s', end)
            logging.debug('being_completed=%s', being_completed)
            logging.debug('words=%s', words)
            
            if not words:
                self.current_candidates = sorted(self.options.keys())
            else:
                try:
                    if begin == 0:
                        # first word
                        candidates = self.options.keys()
                    else:
                        # later word
                        first = words[0]
                        candidates = self.options[first]
                    
                        # dump module
                    if len(words)>1 and words[1] == 'module':
                        candidates = self.validModuleNames
                        
                                
                    if being_completed:
                        # match options with portion of input
                        # being completed
                        self.current_candidates = [ w for w in candidates
                                                    if w.startswith(being_completed) ]

                    else:
                        # matching empty string so use all candidates
                        self.current_candidates = candidates

                    logging.debug('candidates=%s', self.current_candidates)
                    
                except (KeyError, IndexError), err:
                    logging.error('completion error: %s', err)
                    self.current_candidates = []
        
        try:
            response = self.current_candidates[state]
        except IndexError:
            response = None
        logging.debug('complete(%s, %s) => %s', repr(text), state, response)
        return response

        