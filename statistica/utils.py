"""Utility functions and classes for other Statistica modules"""

class InfoList(list):
    """Acts like a normal list but also accepts string keys which serve as metadata"""

    def __init__(self, seq, metadata):
        list.__init__(self, seq)
        self.metadata = dict(metadata)

    def __getitem__(self, key):

        if isinstance(key, int):
            return list.__getitem__(self, key)

        return self.metadata[key]

    def __setitem__(self, key, value):

        if isinstance(key, int):
            list.__setitem__(self, key, value)

        else:
            self.metadata[key] = value
    '''
    def __repr__(self, indent=2):

        return '\n'.join([
            'InfoList(',
            ' '*indent + '\n'.join([
                '[',
                *['\n'.join([' '*indent + ln for ln in repr(self[i]).splitlines()]) for ]
                ']'
            ]) + ','
            ' '*indent + '\n'.join([
                '{',
                *[' '*indent + repr(k) + ': ' + repr(v) for k, v in self.metadata.items()],
                '}'
            ])
        ])
    '''
