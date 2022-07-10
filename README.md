# Recruitment task 2022
Hi! My name is Aleksnadra Janczewska and this is my solution to the recruitment task for the position of Intern Python Developer at Profil Software.

# How to use my script
To run my script type in the word python ( or python3) followed by the path to my script ( email_operations.py), 
then depending on the operartions you want to performe add adequate command:

**1. Show incorrect emails (--incorrect-emails, -ic)**  
    Results in: printing the number of invalid emails, then one invalid email per line.

**2.  Search emails by text (--search str, -s str)**  
     Results in: printing the number of found emails, then one found email per line.

**3. Group emails by domain (--group-by-domain, -gbd)**  
     Results in: grouping emails by one domain and order domains and emails alphabetically.

**4. Find emails that are not in the logs file (--find-emails-not-in-logs path_to_logs_file, -feil path_to_logs_file)**  
     Results in: printing the numbers of found emails that are not in the provided logs file, then one found email per line sorted alphabetically.  
     * A logfile should be formatted as follows:
      `[DATE]: Email has been sent to 'EMAIL'`  
      
 **Examples:**   
  `python email_operations.py -ic ` - will performe in showing incorrect emails  
  `python email_operations.py --search agustin` - will performe in searching emails by text = agustin  
  `python email_operations.py --group-by-domain` - will performe in grouping emails by domain    
  `python email_operations.py -feil email-sent.logs` - will performe in finding emails that are not in the given logs file  
  It is possible to combine those commands in one calling, for example:  
   `python email_operations.py -ic --search agustin`
  
  
  
