import csv


class Settings:
    def __init__(self, file=None):
        self.fields = ['whiteModel128',
                       'blackModel128',
                       'whiteModel',
                       'whitePieceModel',
                       'whiteMoveModel',
                       'blackModel',
                       'blackPieceModel',
                       'blackMoveModel']
        if file:
            self.load_settings(file=file)
        else:
            self.s = {'whiteModel128': False,
                      'blackModel128': False,
                      'whiteModel': None,
                      'whitePieceModel': None,
                      'whiteMoveModel': None,
                      'blackModel': None,
                      'blackPieceModel': None,
                      'blackMoveModel': None}

    def load_settings(self, file):
        with open(file, 'r') as f:
            reader = csv.DictReader(f)
            for r in reader:
                self.s = r

    def save_settings(self, file):
        with open(file, 'w') as f:
            writer = csv.DictWriter(f, self.fields)
            writer.writeheader()
            writer.writerow(self.s)