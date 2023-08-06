from .allnumbers import Numbers as __num__ 


__languages = ['english', 'arabic', 'hindi', 'persian', 'bengali',
             'chinese_simple', 'chinese_complex', 'malayalam', 'thai', 'urdu']

for __language_1 in __languages:
    for __language_2 in __languages:
        if __language_1 != __language_2:
            locals()['{}_to_{}'.format(__language_1, __language_2)] = eval(
                '__num__().{}_to_{}'.format(__language_1, __language_2))
