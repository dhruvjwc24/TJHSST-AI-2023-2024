# Warmup-2
def string_times(str, n): return str*n
def front_times(str, n): return str[:3]*n
def string_bits(str): return str[::2]
def string_splosion(str): return "".join(str[:i+1] for i in range(len(str)))
def last2(str): return sum(str[i:i+2] == str[-2:] for i in range(0, len(str)-2))
def array_count9(nums): return nums.count(9)
def array_front9(nums): return 9 in nums[:4]
def array123(nums): return any(nums[i:i+3] == [1, 2, 3] for i in range(len(nums) - 2))
def string_match(a, b): return sum(a[i:i+2] == b[i:i+2]for i in range(min(len(a), len(b))-1))

# String-2
def double_char(str): return "".join(c*2 for c in str)
def count_hi(str): return str.count("hi") 
def cat_dog(str): return str.count("cat")==str.count("dog")
def count_code(str): return sum(("co" == str[i:i+2] and "e" == str[i+3]) for i in range(len(str)-3))
def end_other(a, b): return (c:=a.lower()).endswith((d:=(b.lower()))) or d.endswith(c)
def xyz_there(str): return "xyz" in "|".join(str.split(".xyz"))

# List-2
def count_evens(nums): return sum(n%2==0 for n in nums)
def big_diff(nums): return max(nums) - min(nums)
def centered_average(nums): return (sum(nums)-max(nums)-min(nums))//(len(nums)-2)
def sum13(nums): return sum(num for i, num in enumerate(nums) if num != 13 and (i == 0 or nums[i - 1] != 13))
def sum67(nums): return sum(x for v, x in enumerate(nums) if ([True, False][6 in nums[0:v + 1]]) or not (-nums[v::-1].index(6)+v)+nums[(-nums[v::-1].index(6) + v):].index(7)>=v)
def has22(nums): return (2, 2) in zip(nums, nums[1:])

# Logic-2
def make_bricks(small, big, goal): return any((g:=(goal-i))%5 == 0 and g/5 <= big for i in range(small+1))
def lone_sum(a,b,c): return sum(x for x in (a, b, c) if (a, b, c).count(x) == 1)
def lucky_sum(a, b, c): return sum([a, b, c][:[a, b, c].index(13)] if 13 in [a, b, c] else [a, b, c])
def no_teen_sum(a, b, c): return sum(x * (x not in [13, 14, 17, 18, 19]) for x in (a, b, c))
def round_sum(a, b, c): return sum(n//10*10 + 10*(n%10 >= 5) for n in (a, b, c))
def close_far(a, b, c): return (((abs(a-b) <= 1 and abs(a-c) >= 2) or (abs(a-c) <= 1 and abs(a-b) >= 2)) and abs(b-c) >= 2)
def make_chocolate(small, big, goal): return [-1, goal - min(goal // 5, big)*5][(goal - (g:=(min(goal // 5, big)*5))) <= small]

#Dhruv Chandna Period 6 2025