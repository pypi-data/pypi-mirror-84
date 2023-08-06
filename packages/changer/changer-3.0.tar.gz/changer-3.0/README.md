# convert_numbers
![Twitter Follow](https://img.shields.io/twitter/follow/Al_Azwari?label=Follow&style=social) [![Downloads](https://pepy.tech/badge/changer)](https://pepy.tech/project/changer) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Django?style=plastic) [![PyPI version](https://badge.fury.io/py/changer.svg)](https://badge.fury.io/py/changer) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/azwri/changer)
##### Changer is - Arabic English Persian Hindi Chinese Malayalam Thai Bengali - Python library to convert numbers from to.


##### Installation

```bash
pip install changer
```

##### Usage

```python
import changer

# From English
print(changer.english_to_arabic('1234567890'))  # ١٢٣٤٥٦٧٨٩٠
print(changer.english_to_hindi('1234567890'))  # ١٢٣٤٥٦٧٨٩٠
print(changer.english_to_persian('1234567890'))  # ۱۲۳۴۵۶۷۸۹۰
print(changer.english_to_bengali('1234567890'))  # ১২৩৪৫৬৭৮৯০
print(changer.english_to_chinese_simple('1234567890'))  # 一二三四五六七八九〇
print(changer.english_to_chinese_complex('1234567890'))  # 貳壹參肆伍陸柒捌玖零
print(changer.english_to_malayalam('1234567890'))  # ൨൧൩൪൫൬൭൮൯൦
print(changer.english_to_thai('1234567890'))  # ๒๑๓๔๕๖๗๘๙๐

# From Arabic
print(changer.arabic_to_english('١٢٣٤٥٦٧٨٩٠'))  # 1234567890
print(changer.arabic_to_hindi('١٢٣٤٥٦٧٨٩٠'))  # ١٢٣٤٥٦٧٨٩٠
print(changer.arabic_to_persian('١٢٣٤٥٦٧٨٩٠'))  # ۱۲۳۴۵۶۷۸۹۰
print(changer.arabic_to_bengali('١٢٣٤٥٦٧٨٩٠'))  # ১২৩৪৫৬৭৮৯০
print(changer.arabic_to_chinese_simple('١٢٣٤٥٦٧٨٩٠'))  # 一二三四五六七八九〇
print(changer.arabic_to_chinese_complex('١٢٣٤٥٦٧٨٩٠'))  # 貳壹參肆伍陸柒捌玖零
print(changer.arabic_to_malayalam('١٢٣٤٥٦٧٨٩٠'))  # ൨൧൩൪൫൬൭൮൯൦
print(changer.arabic_to_thai('١٢٣٤٥٦٧٨٩٠'))  # ๒๑๓๔๕๖๗๘๙๐
print(changer.arabic_to_urdu('١٢٣٤٥٦٧٨٩٠'))  # ۱۲۳۴۵۶۷۸۹۰

# From Hindi
print(changer.hindi_to_english('١٢٣٤٥٦٧٨٩٠'))  # 1234567890
print(changer.hindi_to_arabic('١٢٣٤٥٦٧٨٩٠'))  # 1234567890
print(changer.hindi_to_persian('١٢٣٤٥٦٧٨٩٠'))  # ۱۲۳۴۵۶۷۸۹۰
print(changer.hindi_to_bengali('١٢٣٤٥٦٧٨٩٠'))  # ১২৩৪৫৬৭৮৯০
print(changer.hindi_to_chinese_simple('١٢٣٤٥٦٧٨٩٠'))  # 一二三四五六七八九〇
print(changer.hindi_to_chinese_complex('١٢٣٤٥٦٧٨٩٠'))  # 貳壹參肆伍陸柒捌玖零
print(changer.hindi_to_malayalam('١٢٣٤٥٦٧٨٩٠'))  # ൨൧൩൪൫൬൭൮൯൦
print(changer.hindi_to_thai('١٢٣٤٥٦٧٨٩٠'))  # ๒๑๓๔๕๖๗๘๙๐
print(changer.hindi_to_urdu('١٢٣٤٥٦٧٨٩٠'))  # ۱۲۳۴۵۶۷۸۹۰

# From Persian
print(changer.persian_to_english('۱۲۳۴۵۶۷۸۹۰'))  # 1234567890
print(changer.persian_to_arabic('۱۲۳۴۵۶۷۸۹۰'))  # 1234567890
print(changer.persian_to_hindi('۱۲۳۴۵۶۷۸۹۰'))  # ١٢٣٤٥٦٧٨٩٠
print(changer.persian_to_bengali('۱۲۳۴۵۶۷۸۹۰'))  # ১২৩৪৫৬৭৮৯০
print(changer.persian_to_chinese_simple('۱۲۳۴۵۶۷۸۹۰'))  # 一二三四五六七八九〇
print(changer.persian_to_chinese_complex('۱۲۳۴۵۶۷۸۹۰'))  # 貳壹參肆伍陸柒捌玖零
print(changer.persian_to_malayalam('۱۲۳۴۵۶۷۸۹۰'))  # ൨൧൩൪൫൬൭൮൯൦
print(changer.persian_to_thai('۱۲۳۴۵۶۷۸۹۰'))  # ๒๑๓๔๕๖๗๘๙๐
print(changer.persian_to_urdu('۱۲۳۴۵۶۷۸۹۰'))  # ۱۲۳۴۵۶۷۸۹۰

# From Bengali
print(changer.bengali_to_english('১২৩৪৫৬৭৮৯০'))  # 1234567890
print(changer.bengali_to_arabic('১২৩৪৫৬৭৮৯০'))  # 1234567890
print(changer.bengali_to_hindi('১২৩৪৫৬৭৮৯০'))  # ١٢٣٤٥٦٧٨٩٠
print(changer.bengali_to_persian('১২৩৪৫৬৭৮৯০'))  # ۱۲۳۴۵۶۷۸۹۰
print(changer.bengali_to_chinese_simple('১২৩৪৫৬৭৮৯০'))  # 一二三四五六七八九〇
print(changer.bengali_to_chinese_complex('১২৩৪৫৬৭৮৯০'))  # 貳壹參肆伍陸柒捌玖零
print(changer.bengali_to_malayalam('১২৩৪৫৬৭৮৯০'))  # ൨൧൩൪൫൬൭൮൯൦
print(changer.bengali_to_thai('১২৩৪৫৬৭৮৯০'))  # ๒๑๓๔๕๖๗๘๙๐
print(changer.bengali_to_urdu('১২৩৪৫৬৭৮৯০'))  # ۱۲۳۴۵۶۷۸۹۰

# From Chinese Simple
print(changer.chinese_simple_to_english('一二三四五六七八九〇'))  # 1234567890
print(changer.chinese_simple_to_arabic('一二三四五六七八九〇'))  # 1234567890
print(changer.chinese_simple_to_hindi('一二三四五六七八九〇'))  # ١٢٣٤٥٦٧٨٩٠
print(changer.chinese_simple_to_persian('一二三四五六七八九〇'))  # ۱۲۳۴۵۶۷۸۹۰
print(changer.chinese_simple_to_bengali('一二三四五六七八九〇'))  # ১২৩৪৫৬৭৮৯০
print(changer.chinese_simple_to_chinese_complex('一二三四五六七八九〇'))  # 貳壹參肆伍陸柒捌玖零
print(changer.chinese_simple_to_malayalam('一二三四五六七八九〇'))  # ൨൧൩൪൫൬൭൮൯൦
print(changer.chinese_simple_to_thai('一二三四五六七八九〇'))  # ๒๑๓๔๕๖๗๘๙๐
print(changer.chinese_simple_to_urdu('一二三四五六七八九〇'))  # ۱۲۳۴۵۶۷۸۹۰

# From Chinese Complex
print(changer.chinese_complex_to_english('貳壹參肆伍陸柒捌玖零'))  # 1234567890
print(changer.chinese_complex_to_arabic('貳壹參肆伍陸柒捌玖零'))  # 1234567890
print(changer.chinese_complex_to_hindi('貳壹參肆伍陸柒捌玖零'))  # ١٢٣٤٥٦٧٨٩٠
print(changer.chinese_complex_to_persian('貳壹參肆伍陸柒捌玖零'))  # ۱۲۳۴۵۶۷۸۹۰
print(changer.chinese_complex_to_bengali('貳壹參肆伍陸柒捌玖零'))  # ১২৩৪৫৬৭৮৯০
print(changer.chinese_complex_to_chinese_simple('貳壹參肆伍陸柒捌玖零'))  # 一二三四五六七八九〇
print(changer.chinese_complex_to_malayalam('貳壹參肆伍陸柒捌玖零'))  # ൨൧൩൪൫൬൭൮൯൦
print(changer.chinese_complex_to_thai('貳壹參肆伍陸柒捌玖零'))  # ๒๑๓๔๕๖๗๘๙๐
print(changer.chinese_complex_to_urdu('貳壹參肆伍陸柒捌玖零'))  # ۱۲۳۴۵۶۷۸۹۰

# From Malayalam
print(changer.malayalam_to_english('൨൧൩൪൫൬൭൮൯൦'))  # 1234567890
print(changer.malayalam_to_arabic('൨൧൩൪൫൬൭൮൯൦'))  # 1234567890
print(changer.malayalam_to_hindi('൨൧൩൪൫൬൭൮൯൦'))  # ١٢٣٤٥٦٧٨٩٠
print(changer.malayalam_to_persian('൨൧൩൪൫൬൭൮൯൦'))  # ۱۲۳۴۵۶۷۸۹۰
print(changer.malayalam_to_bengali('൨൧൩൪൫൬൭൮൯൦'))  # ১২৩৪৫৬৭৮৯০
print(changer.malayalam_to_chinese_simple('൨൧൩൪൫൬൭൮൯൦'))  # 一二三四五六七八九〇
print(changer.malayalam_to_chinese_complex('൨൧൩൪൫൬൭൮൯൦'))  # 貳壹參肆伍陸柒捌玖零
print(changer.malayalam_to_thai('൨൧൩൪൫൬൭൮൯൦'))  # ๒๑๓๔๕๖๗๘๙๐
print(changer.malayalam_to_urdu('൨൧൩൪൫൬൭൮൯൦'))  # ۱۲۳۴۵۶۷۸۹۰

# From Thai
print(changer.thai_to_english('๒๑๓๔๕๖๗๘๙๐'))  # 1234567890
print(changer.thai_to_arabic('๒๑๓๔๕๖๗๘๙๐'))  # 1234567890
print(changer.thai_to_hindi('๒๑๓๔๕๖๗๘๙๐'))  # ١٢٣٤٥٦٧٨٩٠
print(changer.thai_to_persian('๒๑๓๔๕๖๗๘๙๐'))  # ۱۲۳۴۵۶۷۸۹۰
print(changer.thai_to_bengali('๒๑๓๔๕๖๗๘๙๐'))  # ১২৩৪৫৬৭৮৯০
print(changer.thai_to_chinese_simple('๒๑๓๔๕๖๗๘๙๐'))  # 一二三四五六七八九〇
print(changer.thai_to_chinese_complex('๒๑๓๔๕๖๗๘๙๐'))  # 貳壹參肆伍陸柒捌玖零
print(changer.thai_to_malayalam('๒๑๓๔๕๖๗๘๙๐'))  # ൨൧൩൪൫൬൭൮൯൦
print(changer.thai_to_urdu('๒๑๓๔๕๖๗๘๙๐'))  # ۱۲۳۴۵۶۷۸۹۰

# From Urdu
print(changer.urdu_to_english('۱۲۳۴۵۶۷۸۹۰'))  # 1234567890
print(changer.urdu_to_arabic('۱۲۳۴۵۶۷۸۹۰'))  # 1234567890
print(changer.urdu_to_hindi('۱۲۳۴۵۶۷۸۹۰'))  # ١٢٣٤٥٦٧٨٩٠
print(changer.urdu_to_persian('۱۲۳۴۵۶۷۸۹۰'))  # ۱۲۳۴۵۶۷۸۹۰
print(changer.urdu_to_bengali('۱۲۳۴۵۶۷۸۹۰'))  # ১২৩৪৫৬৭৮৯০
print(changer.urdu_to_chinese_simple('۱۲۳۴۵۶۷۸۹۰'))  # 一二三四五六七八九〇
print(changer.urdu_to_chinese_complex('۱۲۳۴۵۶۷۸۹۰'))  # 貳壹參肆伍陸柒捌玖零
print(changer.urdu_to_malayalam('۱۲۳۴۵۶۷۸۹۰'))  # ൨൧൩൪൫൬൭൮൯൦
print(changer.urdu_to_thai('۱۲۳۴۵۶۷۸۹۰'))  # ๒๑๓๔๕๖๗๘๙๐
```

## Contributing
Please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)