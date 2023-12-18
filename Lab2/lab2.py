def make_chocolate(small, big, goal):
  #return min([num for num in [goal-5*i if goal - 5*i <= small else 1000 for i in range(big+1)] if num >=0])
  return [goal-5*i if goal - 5*i <= small else 1000 for i in range(big+1)]

def count_code(str):
  return sum([("co" == str[i:i+2] and "e" == str[i+3]) for i in range(len(str)-3)])


def double_char(str):
    return "".join([char*2 for char in str])

def lone_sum(a,b,c):
  return sum(x for x in (a, b, c) if (a, b, c).count(x) == 1)

def no_teen_sum(a, b, c):
    return sum([x * (x not in [13, 14, 17, 18, 19]) for x in (a, b, c)])

#print(no_teen_sum(19, 15, 13))

def sum_13(nums):
   return (2, 2) in [z for z in zip(nums, nums[1:])]

def end_other(a, b):
  #return a.lower().endswith(b.lower()) or b.lower().endswith(a.lower())
  print(max(a, b))
  print(min(a, b))
  return max(a, b, key=len).endswith(min(a, b, key=len))

print(end_other('abc', 'abXabc'))

#print(lone_sum(3, 2, 3))
# def no_teen_sum(a, b, c):
#   return sum({a, b, c} - {13, 14, 17, 18, 19})

# def xyz_there(str):
#   #return str.split(".xyz")

#   #return "xyz" in str.split(".xyz")

def xyz_there(str):
   return any([str.split(".xyz")[i].__contains__("xyz") for i in range(len(str.split(".xyz")))])
    #return str.split(".xyz")

#print(xyz_there('.aa.zaxyb..xy.xyzzz.zbbbxy'))

def sum67(nums):
    #return sum(num for num in nums if not (num == 6 or nums[nums.index(num):].count(7) > 0))
    return sum(nums) - sum(nums[nums.index(6):nums.index(7)+1]) if 6 in nums else sum(nums)


# def lucky_sum(a, b, c):
#   #return a if (b==13 and not(a==13)) else a+b if (c==13 and (not(13 in [a, b]))) else a+b+c if not(13 in [a, b, c]) else 0
#   return sum([a, b, c]) if not 13 in [a, b, c] else sum([a, b, c]) - sum([a, b, c][[a, b, c].index(13):[a, b, c].index(13)+2])

# def lucky_sum(a, b, c):
#   #return try [a, b, c].index(13) except 
#   return sum(if 13 in [a, b, c] [a, b, c][:[a, b, c].index(13)] )


# def make_bricks(small, big, goal):
#   return any([(goal-i)%5 == 0 and (goal-i)/5 <= big for i in range(small+1)])
 
def make_bricks(small, big, goal):
  return any([(g:=(goal-i))%5 == 0 and g/5 <= big for i in range(small+1)])

def make_chocolate(small, big, goal):
  return goal - g if (goal - (g:=(min(goal // 5, big)*5))) <= small else -1

#print(make_chocolate(7, 0, 9))
# nums = [1, 2, 1, 2]
# l = "22" in "".join([str(i) for i in nums])
# print(l)

def no_teen_sum(a, b, c):
    return sum([x if x not in [13, 14, 17, 18, 19] else 0 for x in (a, b, c)])



def has22(nums):
  #return any([2 == nums[i] and 2 == nums[i+1] for i in range(len(nums)-1)])
  return any([[2, 2] == nums[i:i+2] for i in range(len(nums)-1)])
#print(round_sum(8, 25, 75))
#print(has22([1, 2, 1, 2]))


def xyz_there(str):
   #return any(["xyz" in str.split(".xyz")[i] for i in range(len(str.split(".xyz")))])
   #return "xyz" in "".join(str.split(".xyz"))
   return "|".join(str.split(".xyz"))
#print(xyz_there('aa.yyzxxaxy.xyzzxazzyb.az'))

def make_bricks(small, big, goal):
  return ((g:=goal // 5) <= big) and (goal % (5*g) <= small)

def func(nums):
  return sum([x for i, x in enumerate(nums) if (((nums[(i - nums[i::-1].index(6)):].index(7) + (i - nums[i::-1].index(6))) < i) if (6 in nums[:i+1]) else True)])

def end_other(a, b):
  return max(a, b, key=len).lower().endswith(min(a, b, key=len).lower())
  return a.lower().endswith(b.lower()) or b.lower().endswith(a.lower())
  return (c:=a.lower()).endswith((d:=(b.lower()))) or d.endswith(c)

#print(end_other('abc', 'abXabc'))

def lucky_sum(a, b, c):
  print([a, b, c][:[a, b, c, 13].index(13)])
  print(13*int([a, b, c, 13].index(13)==3))
  #return(13*int([a, b, c, 13].index(13)==3))
  return sum([a, b, c][:[a, b, c, 13].index(13)] - 13*int([a, b, c, 13].index(13)==3))

print(lucky_sum(1, 2, 3))


