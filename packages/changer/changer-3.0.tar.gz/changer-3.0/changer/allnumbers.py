class Numbers:
    def __init__(self):

        # english
        self.__engilsh = (
        ('1', '١'),
        ('2', '٢'),
        ('3', '٣'),
        ('4', '٤'),
        ('5', '٥'),
        ('6', '٦'),
        ('7', '٧'),
        ('8', '٨'),
        ('9', '٩'),
        ('0', '٠'),
        )

        # arabic
        self.__arabic = (
        ('١', '1'),
        ('٢', '2'),
        ('٣', '3'),
        ('٤', '4'),
        ('٥', '5'),
        ('٦', '6'),
        ('٧', '7'),
        ('٨', '8'),
        ('٩', '9'),
        ('٠', '0'),
        )

        # hindi
        self.__hindi = (
        ('١', '1'),
        ('٢', '2'),
        ('٣', '3'),
        ('٤', '4'),
        ('٥', '5'),
        ('٦', '6'),
        ('٧', '7'),
        ('٨', '8'),
        ('٩', '9'),
        ('٠', '0'),
        )
        # persian
        self.__persian = (
        ('۱', '1'),
        ('۲', '2'),
        ('۳', '3'),
        ('۴', '4'),
        ('۵', '5'),
        ('۶', '6'),
        ('۷', '7'),
        ('۸', '8'),
        ('۹', '9'),
        ('۰', '0'),
        )

        #bengali
        self.__bengali = (
        ('১', '1'),
        ('২', '2'),
        ('৩', '3'),
        ('৪', '4'),
        ('৫', '5'),
        ('৬', '6'),
        ('৭', '7'),
        ('৮', '8'),
        ('৯', '9'),
        ('০', '0'),
        )

        #chinese_simple
        self.__chinese_simple = (
        ('一', '1'),
        ('二', '2'),
        ('三', '3'),
        ('四', '4'),
        ('五', '5'),
        ('六', '6'),
        ('七', '7'),
        ('八', '8'),
        ('九', '9'),
        ('〇', '0'),
        )

        #chinese_complex
        self.__chinese_complex = (
        ('壹', '1'),
        ('貳', '2'),
        ('參', '3'),
        ('肆', '4'),
        ('伍', '5'),
        ('陸', '6'),
        ('柒', '7'),
        ('捌', '8'),
        ('玖', '9'),
        ('零', '0'),
        )

        #chinese_malayalam
        self.__malayalam = (
        ('൧', '1'),
        ('൨', '2'),
        ('൩', '3'),
        ('൪', '4'),
        ('൫', '5'),
        ('൬', '6'),
        ('൭', '7'),
        ('൮', '8'),
        ('൯', '9'),
        ('൦', '0'),
        )

        #__thai
        self.__thai = (
        ('๑', '1'),
        ('๒', '2'),
        ('๓', '3'),
        ('๔', '4'),
        ('๕', '5'),
        ('๖', '6'),
        ('๗', '7'),
        ('๘', '8'),
        ('๙', '9'),
        ('๐', '0'),
        )

        #__urdu
        self.__urdu = (
        ('۱', '1'),
        ('۲', '2'),
        ('۳', '3'),
        ('۴', '4'),
        ('۵', '5'),
        ('۶', '6'),
        ('۷', '7'),
        ('۸', '8'),
        ('۹', '9'),
        ('۰', '0'),
        )

# ##################################################

    def __to_change_1(self, __language, numbers):
        num = []
        if isinstance(numbers, int):
            numbers = str(numbers)
        for i in enumerate(numbers):
            for n in __language:
                if i[1] in n:
                    num.append(n[0])
        return ''.join(map(str, num))
    
    def __to_change_2(self, __language, numbers):
        num = []
        if isinstance(numbers, int):
            numbers = str(numbers)
        for i in enumerate(numbers):
            for n in __language:
                if i[1] in n:
                    num.append(n[1])
        return ''.join(map(str, num))
    

    # From English
    english_to_arabic = lambda self, the_number : self.__to_change_1(self.__arabic, numbers=the_number)
    english_to_hindi = lambda self, the_number : self.__to_change_1(self.__hindi, numbers=the_number)
    english_to_persian = lambda self, the_number : self.__to_change_1(self.__persian, numbers=the_number)
    english_to_bengali = lambda self, the_number : self.__to_change_1(self.__bengali, numbers=the_number)
    english_to_chinese_simple = lambda self, the_number : self.__to_change_1(self.__chinese_simple, numbers=the_number)
    english_to_chinese_complex = lambda self, the_number : self.__to_change_1(self.__chinese_complex, numbers=the_number)
    english_to_malayalam = lambda self, the_number : self.__to_change_1(self.__malayalam, numbers=the_number)
    english_to_thai = lambda self, the_number : self.__to_change_1(self.__thai, numbers=the_number)
    english_to_urdu = lambda self, the_number : self.__to_change_1(self.__urdu, numbers=the_number)

    # From Arabic
    arabic_to_english = lambda self, the_number : self.__to_change_2(self.__arabic, numbers=the_number)
    arabic_to_hindi = lambda self, the_number : self.english_to_hindi(self.arabic_to_english(the_number))
    arabic_to_persian = lambda self, the_number : self.english_to_persian(self.arabic_to_english(the_number))
    arabic_to_bengali = lambda self, the_number : self.english_to_bengali(self.arabic_to_english(the_number))
    arabic_to_chinese_simple = lambda self, the_number : self.english_to_chinese_simple(self.arabic_to_english(the_number))
    arabic_to_chinese_complex = lambda self, the_number : self.english_to_chinese_complex(self.arabic_to_english(the_number))
    arabic_to_malayalam = lambda self, the_number : self.english_to_malayalam(self.arabic_to_english(the_number))
    arabic_to_thai = lambda self, the_number : self.english_to_thai(self.arabic_to_english(the_number))
    arabic_to_urdu = lambda self, the_number : self.english_to_urdu(self.arabic_to_english(the_number))


    # From Hindi
    hindi_to_english = lambda self, the_number : self.__to_change_2(self.__hindi, numbers=the_number)
    hindi_to_arabic = lambda self, the_number : self.arabic_to_english(self.hindi_to_english(the_number))
    hindi_to_persian = lambda self, the_number : self.english_to_persian(self.hindi_to_english(the_number))
    hindi_to_bengali = lambda self, the_number : self.english_to_bengali(self.hindi_to_english(the_number))
    hindi_to_chinese_simple = lambda self, the_number : self.english_to_chinese_simple(self.hindi_to_english(the_number))
    hindi_to_chinese_complex = lambda self, the_number : self.english_to_chinese_complex(self.hindi_to_english(the_number))
    hindi_to_malayalam = lambda self, the_number : self.english_to_malayalam(self.hindi_to_english(the_number))
    hindi_to_thai = lambda self, the_number : self.english_to_thai(self.hindi_to_english(the_number))
    hindi_to_urdu = lambda self, the_number : self.english_to_urdu(self.hindi_to_english(the_number))

    # From Persian
    persian_to_english = lambda self, the_number : self.__to_change_2(self.__persian, numbers=the_number)
    persian_to_arabic = lambda self, the_number : self.arabic_to_english(self.persian_to_english(the_number))
    persian_to_hindi = lambda self, the_number : self.english_to_hindi(self.persian_to_english(the_number))
    persian_to_bengali = lambda self, the_number : self.english_to_bengali(self.persian_to_english(the_number))
    persian_to_chinese_simple = lambda self, the_number : self.english_to_chinese_simple(self.persian_to_english(the_number))
    persian_to_chinese_complex = lambda self, the_number : self.english_to_chinese_complex(self.persian_to_english(the_number))
    persian_to_malayalam = lambda self, the_number : self.english_to_malayalam(self.persian_to_english(the_number))
    persian_to_thai = lambda self, the_number : self.english_to_thai(self.persian_to_english(the_number))
    persian_to_urdu = lambda self, the_number : self.english_to_urdu(self.persian_to_english(the_number))

    # From Bengali
    bengali_to_english = lambda self, the_number : self.__to_change_2(self.__bengali, numbers=the_number)
    bengali_to_arabic = lambda self, the_number : self.arabic_to_english(self.bengali_to_english(the_number))
    bengali_to_hindi = lambda self, the_number : self.english_to_hindi(self.bengali_to_english(the_number))
    bengali_to_persian = lambda self, the_number : self.english_to_persian(self.bengali_to_english(the_number))
    bengali_to_chinese_simple = lambda self, the_number : self.english_to_chinese_simple(self.bengali_to_english(the_number))
    bengali_to_chinese_complex = lambda self, the_number : self.english_to_chinese_complex(self.bengali_to_english(the_number))
    bengali_to_malayalam = lambda self, the_number : self.english_to_malayalam(self.bengali_to_english(the_number))
    bengali_to_thai = lambda self, the_number : self.english_to_thai(self.bengali_to_english(the_number))
    bengali_to_urdu = lambda self, the_number : self.english_to_urdu(self.bengali_to_english(the_number))

    # From Chinese Simple
    chinese_simple_to_english = lambda self, the_number : self.__to_change_2(self.__chinese_simple, numbers=the_number)
    chinese_simple_to_arabic = lambda self, the_number : self.arabic_to_english(self.chinese_simple_to_english(the_number))
    chinese_simple_to_hindi = lambda self, the_number : self.english_to_hindi(self.chinese_simple_to_english(the_number))
    chinese_simple_to_persian = lambda self, the_number : self.english_to_persian(self.chinese_simple_to_english(the_number))
    chinese_simple_to_bengali = lambda self, the_number : self.english_to_bengali(self.chinese_simple_to_english(the_number))
    chinese_simple_to_chinese_complex = lambda self, the_number : self.english_to_chinese_complex(self.chinese_simple_to_english(the_number))
    chinese_simple_to_malayalam = lambda self, the_number : self.english_to_malayalam(self.chinese_simple_to_english(the_number))
    chinese_simple_to_thai = lambda self, the_number : self.english_to_thai(self.chinese_simple_to_english(the_number))
    chinese_simple_to_urdu = lambda self, the_number : self.english_to_urdu(self.chinese_simple_to_english(the_number))

    # From Chinese Complex
    chinese_complex_to_english = lambda self, the_number : self.__to_change_2(self.__chinese_complex, numbers=the_number)
    chinese_complex_to_arabic = lambda self, the_number : self.arabic_to_english(self.chinese_complex_to_english(the_number))
    chinese_complex_to_hindi = lambda self, the_number : self.english_to_hindi(self.chinese_complex_to_english(the_number))
    chinese_complex_to_persian = lambda self, the_number : self.english_to_persian(self.chinese_complex_to_english(the_number))
    chinese_complex_to_bengali = lambda self, the_number : self.english_to_bengali(self.chinese_complex_to_english(the_number))
    chinese_complex_to_chinese_simple = lambda self, the_number : self.english_to_chinese_simple(self.chinese_complex_to_english(the_number))
    chinese_complex_to_malayalam = lambda self, the_number : self.english_to_malayalam(self.chinese_complex_to_english(the_number))
    chinese_complex_to_thai = lambda self, the_number : self.english_to_thai(self.chinese_complex_to_english(the_number))
    chinese_complex_to_urdu = lambda self, the_number : self.english_to_urdu(self.chinese_complex_to_english(the_number))

    # From Malayalam
    malayalam_to_english = lambda self, the_number : self.__to_change_2(self.__malayalam, numbers=the_number)
    malayalam_to_arabic = lambda self, the_number : self.arabic_to_english(self.malayalam_to_english(the_number))
    malayalam_to_hindi = lambda self, the_number : self.english_to_hindi(self.malayalam_to_english(the_number))
    malayalam_to_persian = lambda self, the_number : self.english_to_persian(self.malayalam_to_english(the_number))
    malayalam_to_bengali = lambda self, the_number : self.english_to_bengali(self.malayalam_to_english(the_number))
    malayalam_to_chinese_simple = lambda self, the_number : self.english_to_chinese_simple(self.malayalam_to_english(the_number))
    malayalam_to_chinese_complex = lambda self, the_number : self.english_to_chinese_complex(self.malayalam_to_english(the_number))
    malayalam_to_thai = lambda self, the_number : self.english_to_thai(self.malayalam_to_english(the_number))
    malayalam_to_urdu = lambda self, the_number : self.english_to_urdu(self.malayalam_to_english(the_number))

    # From Thai
    thai_to_english = lambda self, the_number : self.__to_change_2(self.__thai, numbers=the_number)
    thai_to_arabic = lambda self, the_number : self.arabic_to_english(self.thai_to_english(the_number))
    thai_to_hindi = lambda self, the_number : self.english_to_hindi(self.thai_to_english(the_number))
    thai_to_persian = lambda self, the_number : self.english_to_persian(self.thai_to_english(the_number))
    thai_to_bengali = lambda self, the_number : self.english_to_bengali(self.thai_to_english(the_number))
    thai_to_chinese_simple = lambda self, the_number : self.english_to_chinese_simple(self.thai_to_english(the_number))
    thai_to_chinese_complex = lambda self, the_number : self.english_to_chinese_complex(self.thai_to_english(the_number))
    thai_to_malayalam = lambda self, the_number : self.english_to_malayalam(self.thai_to_english(the_number))
    thai_to_urdu = lambda self, the_number : self.english_to_urdu(self.thai_to_english(the_number))

    # From Urdu
    urdu_to_english = lambda self, the_number : self.__to_change_2(self.__urdu, numbers=the_number)
    urdu_to_arabic = lambda self, the_number : self.arabic_to_english(self.urdu_to_english(the_number))
    urdu_to_hindi = lambda self, the_number : self.english_to_hindi(self.urdu_to_english(the_number))
    urdu_to_persian = lambda self, the_number : self.english_to_persian(self.urdu_to_english(the_number))
    urdu_to_bengali = lambda self, the_number : self.english_to_bengali(self.urdu_to_english(the_number))
    urdu_to_chinese_simple = lambda self, the_number : self.english_to_chinese_simple(self.urdu_to_english(the_number))
    urdu_to_chinese_complex = lambda self, the_number : self.english_to_chinese_complex(self.urdu_to_english(the_number))
    urdu_to_thai = lambda self, the_number : self.english_to_thai(self.urdu_to_english(the_number))
    urdu_to_malayalam = lambda self, the_number : self.english_to_malayalam(self.urdu_to_english(the_number))


# ##################################################
    # def arabic_to_hindi(self, n):
    #     n = self.arabic_to_english(n)
    #     return self.english_to_hindi(n)


    # def english_to_arabic(self, language):
    #     return self.to_change(self.__arabic)
    

    # def english_to_arabic(self, numbers):
    #     num = []
    #     if isinstance(numbers, int):
    #         numbers = str(numbers)
    #     for i in enumerate(numbers):
    #         for n in self.__arabic:
    #             if i[1] in n:
    #                 num.append(n[1])
    #     return ''.join(map(str, num))
# ##################################################