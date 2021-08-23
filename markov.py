from random import choice

class MarkovChain:

    def __init__(self, filename, chunksize):
        self.filename = filename
        self.chunksize = chunksize
        self.markov_chain, self.starters = self.create_markov_chain()

    # chunksize determines how close to the original the generated text is (the higher the value the closer it is)
    def create_markov_chain(self):

        with open(self.filename, 'r') as f:
            all_data = f.readlines()

        d = {}
        starters = []
        n = self.chunksize

        for piece in all_data:

            starters.append(piece[0:n])

            # iterate through one line and add the chunk to the corresponding dictionary
            for i in range(len(piece)-n-1):

                chunk = piece[i:(i+n)]
                
                if chunk not in d:
                    d[chunk] = []
                    
                d[chunk].append(piece[i+n])

        return(d, starters)

    def generate_text(self):
        o = ''
        end_of_sentence = ['.','!','?']

        nex = choice(self.starters)
        o = nex+choice(self.markov_chain[nex])
        nex = o[(len(o)-self.chunksize):]

        while True:
            try:
                o+=choice(self.markov_chain[nex])
                if o[-1] == '\n':
                    break
                nex = o[(len(o)-self.chunksize):]
            except:
                for e in end_of_sentence:
                    if e in o:
                        o = o[:o.index(e)+1]
                        break
                break

        return(o)

markov = MarkovChain
