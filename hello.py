import os

if '__file__' in locals():
    if locals()['__file__'] == '<input>':
        del locals()['__file__']
    else:
        print('hola')
else:
    print('al fin')

'__file__' in locals()