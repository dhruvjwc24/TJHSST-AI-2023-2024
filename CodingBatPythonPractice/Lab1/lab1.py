# Warmup-1
def sleep_in(weekday, vacation): return True if vacation else False if weekday else True
def monkey_trouble(a_smile, b_smile): return True if a_smile == b_smile else False
def sum_double(a, b): return a + b if a != b else 2 * (a+b)
def diff21(n): return abs(21-n)*2 if n>21 else abs(21-n)
def parrot_trouble(talking, hour): return True if(talking and (hour < 7 or hour> 20)) else False
def makes10(a, b): return True if (a == 10 or b == 10 or a+b == 10) else False
def near_hundred(n): return True if (abs(100 - n) <= 10 or abs(200 - n) <= 10) else False
def pos_neg(a, b, negative): return True if (negative and (a < 0 and b < 0)) else True if (not(negative) and (a < 0 and b > 0 or a > 0 and b < 0)) else False

# String-1
def hello_name(name): return "Hello " + name + "!"
def make_abba(a, b): return a + b*2 + a
def make_tags(tag, word): return "<" + tag + ">" + word + "<" + "/" +tag + ">"
def make_out_word(out, word): return out[:len(out)//2] + word + out[len(out)//2:]
def extra_end(str): return 3 * str[-2:]
def first_two(str): return str[:2] if len(str) > 2 else str
def first_half(str): return str[:len(str)//2]
def without_end(str): return str[1:-1]

# List-1
def first_last6(nums): return True if (isinstance(nums[0], int) and (nums[0] == 6 or nums[-1] == 6)) else True if (nums[0] == '6' or nums[-1] == '6') else False
def same_first_last(nums): return len(nums)>0 and nums[0]==nums[-1]
def make_pi(n=3): return [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7, 9, 3, 2, 3, 8][:n]
def common_end(a, b): return a[0] == b[0] or a[-1] == b[-1]
def sum3(nums): return sum(nums)
def rotate_left3(nums): return nums[1:] + nums[:1]
def reverse3(nums): return nums[::-1]
def max_end3(nums): return nums[:1] * len(nums) if nums[0] > nums[-1] else nums[-1:] * len(nums) 

# Logic-1
def cigar_party(cigars, is_weekend): return cigars >= 40 if is_weekend else cigars >= 40 and cigars <= 60
def date_fashion(you, date): return 0 if you <= 2 or date <= 2 else 2 if you >= 8 or date >= 8 else 1
def squirrel_play(temp, is_summer): return False if temp < 60 else True if ((not(is_summer) and temp <= 90) or (is_summer and temp <= 100)) else False
def caught_speeding(speed, is_birthday): return 0 if ((is_birthday and speed <= 65) or (not(is_birthday) and speed<=60)) else 1 if ((is_birthday and speed <= 85) or (not(is_birthday) and speed<=81)) else 2 
def sorta_sum(a, b): return 20 if(a + b >= 10 and a + b <= 19) else a+b
def alarm_clock(day, vacation): return "off" if (vacation and (day % 6 == 0)) else "7:00" if (not(day % 6 == 0) and not(vacation)) else "10:00"
def love6(a, b): return (a == 6 or b == 6) or (abs(a-b) == 6) or (a+b == 6)
def in1to10(n, outside_mode): return n <= 1 or n >= 10 if outside_mode else n >= 1 and n <= 10

#Dhruv Chandna Period 6 2025