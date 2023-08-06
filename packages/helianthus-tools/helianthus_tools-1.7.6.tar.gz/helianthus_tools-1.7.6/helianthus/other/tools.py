# -*- coding: UTF-8 -*-
import os

def f2x(filepath) -> str:
    result = ""
    with open(filepath, "rb") as f:
        for _ in range(os.path.getsize(filepath)):
            item = str(hex(ord(f.read(1))))
            item = r"\x" + item[2:].rjust(2, "0").upper()
            result += item
    return result

def reverse_shellcode(shellcode) -> None:
    shellcode_lenght = len(shellcode)
    print("int buf[%d] = {" %shellcode_lenght)
    for index, i in enumerate(shellcode[::-1]):
        print("0x" + str(hex(ord(i)))[2:].rjust(2, "0").upper(), end=", ")
        index += 1
        if index % 7 == 0:
            print()
    print()
    print("};")


def chinese2arabic(c) -> float:
	# constants for chinese_to_arabic
	CN_NUM = {
	    '〇': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '零': 0,
	    '壹': 1, '贰': 2, '叁': 3, '肆': 4, '伍': 5, '陆': 6, '柒': 7, '捌': 8, '玖': 9, '貮': 2, '两': 2,
	}

	CN_UNIT = {
	    '十': 10,
	    '拾': 10,
	    '百': 100,
	    '佰': 100,
	    '千': 1000,
	    '仟': 1000,
	    '万': 10000,
	    '萬': 10000,
	    '亿': 100000000,
	    '億': 100000000,
	    '兆': 1000000000000,
	}

	def processor(cn: str) -> int:
	    unit = 0  # current
	    ldig = []  # digest
	    for cndig in reversed(cn):
	        if cndig in CN_UNIT:
	            unit = CN_UNIT.get(cndig)
	            if unit == 10000 or unit == 100000000:
	                ldig.append(unit)
	                unit = 1
	        else:
	            dig = CN_NUM.get(cndig)
	            if unit:
	                dig *= unit
	                unit = 0
	            ldig.append(dig)
	    if unit == 10:
	        ldig.append(10)
	    val, tmp = 0, 0
	    for x in reversed(ldig):
	        if x == 10000 or x == 100000000:
	            val += tmp * x
	            tmp = 0
	        else:
	            tmp += x
	    val += tmp
	    return val

	# ALL
	def cn2a(i):
	    flag = False

	    # 判断是否是单独的几分钱
	    if len(i) == 2 and i[-1] == "分":
	        flag = True

	    left = ""
	    right = ""
	    if "元" not in i:
	        left = ""
	        right = i
	    else:
	        left = i.split("元")[0]
	        right = i.split("元")[1]
	    right = right.replace("角", "").replace("分", "").replace("整", "")

	    joinRight = ""
	    for j in list(right):
	        joinRight += str(CN_NUM[j])

	    result = float(str(processor(left)) + "." + joinRight)

	    echoResult = 0

	    if flag:
	        echoResult = round(result / 10, 2)
	    else:
	        echoResult = result
	    return echoResult
	return cn2a(c)