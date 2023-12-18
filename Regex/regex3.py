import sys; args = sys.argv[1:]

solutions = {
                "30" : "/^0$|^10[01]$/", 
                "31" : "/^[01]*$/", 
                "32" : "/0$/", 
                "33" : "/\w*[aeiou]\w*[aeiou]\w*/i", 
                "34" : "/^0$|^1[01]*0$/", 
                "35" : "/^[01]*110[01]*$/", 
                "36" : "/^.{2,4}$/s", 
                "37" : "/^\d{3} *-? *\d\d *-? *\d{4}$/", 
                "38" : "/^.*?d\w*/mi", 
                "39" : "/^[01]?$|^0[01]*0$|^1[01]*1$/",
                
                "40" : "/^[X.O]{64}$/i",
                "41" : "/^[XO]*\.[XO]*$/i",
                "42" : "/^\.|\.$|^x+o*\.|\.o*x+$/i",
                "43" : "/^.(.{2})*$/s",                    
                "44" : "/^(0([01]{2})*|1[01]([01]{2})*)$/",                 
                "45" : "/\w*(a[eiou]|e[aiou]|i[aeou]|o[aeiu]|u[aeio])\w*/i",
                "46" : "/^(1?0+)*1*$/",
                "47" : "/^[bc]*[abc][bc]*$/",
                "48" : "/^((([bc]*a){2}[bc]*)+|[bc]+)$/",
                "49" : "/^(2([02]*(1[02]*){2})*[02]*|((1[02]*){2})+)$/",
             
                "50" : r"/(\w)*\w*\1\w*/i",
                "51" : r"/(\w)*(\w*\1){3}\w*/i",
                "52" : r"/^(0|1)([01]*\1)*$/",
                "53" : r"/\b(?=\w*cat)\w{6}\b/i",
                "54" : r"/\b(?=\w*bri)(?=\w*ing)\w{5,9}\b/i",
                "55" : r"/\b(?!\w*cat)\w{6}\b/i",
                "56" : r"/(?!\w*?(\w)\w*\1)\w+\b/i",
                "57" : r"/^(1(?!0011)|0)*$/",
                "58" : r"/\w*([aeiou])(?!\1)[aeiou]\w*/i",
                "59" : r"/^(?!.*1.1)[01]*$/",
            }
            

print(solutions[args[0]])

#Dhruv Chandna Period 6 2025