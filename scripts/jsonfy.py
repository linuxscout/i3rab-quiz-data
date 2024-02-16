#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  jsonfy.py
#  
#  Copyright 2024 zerrouki <zerrouki@majd4>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#
import json
import argparse
import sys
import os
import pprint
import re
from collections import Counter
def grabargs():
    parser = argparse.ArgumentParser(description='Test Grammar data set builder Analex.')
    # add file name to import and filename to export
    
    parser.add_argument("-f", dest="filename", required=True,
    help="input file to convert", metavar="FILE")
    
    parser.add_argument("-o", dest="outfile", nargs='?', 
    help="Output file to convert", metavar="OUT_FILE")
    parser.add_argument("-l", dest="limit", type=int, nargs='?', default=0, 
    help="limit lines to treat", metavar="LIMIT")
   
    args = parser.parse_args()
    return args

text= """البستان جميل. ;nou nou;mbtd khbr
الْحَديقَةُ جميلةٌ. ;nou nou;mbtd khbr
السَّماءُ مُمْطرَةٌ. ;nou nou;mbtd khbr
الشمس طالعة. ;nou nou;mbtd khbr
الطَّائرُ فَوْقَ الشَّجرَةِ. ;nou tool nou;mbtd pplace added
الْمِدادُ في الدَّوَاةِ. ;nou tool nou;mbtd jar mjror
الْبُسْتانيُّ يَجْمَعُ الأَزهارَ. ;nou vrb nou;mbtd vrb obj
الثَّعْلَبُ يأْكلُ الدَّجاجَ. ;nou vrb nou;mbtd vrb obj
الثَّوْرُ يَحْرُثُ الأَرْضَ. ;nou vrb nou;mbtd vrb obj
عليٌّ يرْكَبُ الحِمَارَ. ;nou vrb nou;mbtd vrb obj
التمر يتَساقطُ عَلى الأَرضِ. ;nou vrb tool nou;mbtd vrb jar mjror
الحَديدُ يَذوبُ في النار. ;nou vrb tool nou;mbtd vrb jar mjror
العُصْفورُ يُغَرِّدُ عَلَى الشجرَةِ.;nou vrb tool nou;mbtd vrb jar mjror
الْكلْبُ يَنامُ في البستان. ;nou vrb tool nou;mbtd vrb jar mjror
فَريدٌ يجْرِي في الشارع. ;nou vrb tool nou;mbtd vrb jar mjror
هل تحب السفر؟ ;tool vrb nou;
لم يتغذَّ الغلام.;tool vrb nou;jazm vrb sbj
لم أخشَ البرد.;tool vrb nou;jazm vrb obj
لا تنسَ وعدك.;tool vrb nou;jazm vrb obj
لم يصفُ الجو.;tool vrb nou;jazm vrb sbj
لم يعدُ الحصان.;tool vrb nou;jazm vrb sbj
لم أشتهِ الطعام.;tool vrb nou;jazm vrb obj
لم يجرِ الماء.;tool vrb nou;jazm vrb sbj
لم يعوِ الذئب. ;tool vrb nou;jazm vrb sbj
لا تدنُ من الكبش.;tool vrb tool nou;jazm vrb jar mjror
سمعت النصيحة. ;vrb nou;vrb obj
يحترق الحطب. ;vrb nou;vrb sbj
يستمع النصيحة.;vrb nou;vrb obj
يطبخ الطَعام.;vrb nou;vrb obj
يُعلّم الأطفال.;vrb nou;vrb obj
يفتح الشبابيك.;vrb nou;vrb obj
يُغلِق الأبواب.;vrb nou;vrb obj
يَفرش البسط.;vrb nou;vrb obj
يشعل المصابيح. ;vrb nou;vrb obj
تجِفُّ الأَرْضُ. ;vrb nou ;vrb sbj
تَطْلُعُ الشَّمْسُ. ;vrb nou ;vrb sbj
يسِيرُ السَّحابُ. ;vrb nou ;vrb sbj
يَنقطِعُ المطرُ. ;vrb nou ;vrb sbj
افتَرَس الذِّئْبُ كبْشاً.;vrb nou nou;vrb sbj obj
ركب إبراهيم الحصان. ;vrb nou nou;vrb sbj obj
شم عليٌّ وردة. ;vrb nou nou;vrb sbj obj
قطف محمد زهرة. ;vrb nou nou;vrb sbj obj
يَتَسَلَّقُ الْغِلْمَانُ الْجَبَل. ;vrb nou nou;vrb sbj obj
يُحِبُّ الْوَلدُ الْبُرْتُقالَ. ;vrb nou nou;vrb sbj obj
يحصد الفلاح القمح. ;vrb nou nou;vrb sbj obj
يداعب إسماعيل القط. ;vrb nou nou;vrb sbj obj
يزْرَعُ الْفلاحُ الْقَصَبَ. ;vrb nou nou;vrb sbj obj
يَشْترِي التاجرُ الْقُطنَ. ;vrb nou nou;vrb sbj obj
يَفْتَحُ محمدٌ الْبابَ. ;vrb nou nou;vrb sbj obj
يَقْرأُ سَعيدٌ الكتَابَ. ;vrb nou nou;vrb sbj obj
يقطِفُ علِيٌّ الأَزهارَ. ;vrb nou nou;vrb sbj obj
يَلْعبُ الْغِلْمانُ بالكُرةِ. ;vrb nou nou;vrb sbj jar mjror
تأكل الشاة فولا و شعيرا. ;vrb nou nou tool nou;vrb sbj obj conj conjd
;vrb sbj jar mjror
يَذْهَبُ العُمَّالُ إلى المصْنَع. ;vrb nou tool nou;vrb sbj jar mjror
يَسْبَحُ الأَوْلادُ في البحر. ;vrb nou tool nou;vrb sbj jar mjror
تجري السفينة على الماء. ;vrb nou tool nou;vrb sbj jar mjror
تسير السفن في الْبحارِ. ;vrb nou tool nou;vrb sbj jar mjror
تصنع الأحذية من الجِلْدِ. ;vrb nou tool nou;vrb sbj jar mjror
يستطع النور في الحجرة. ;vrb nou tool nou;vrb sbj jar mjror
يَشْتَدُّ الْبَرْدُ فَوْقَ الجبالِ. ;vrb nou tool nou;vrb sbj jar mjror
يعيش السمك في الماء. ;vrb nou tool nou;vrb sbj jar mjror
يكثر النخيل في مصر;vrb nou tool nou;vrb sbj jar mjror
ينزل المطر من السماء. ;vrb nou tool nou;vrb sbj jar mjror"""

ERROR_IVALID_LINE = -1
ERROR_IVALID_TAG = -2
ERROR_TAGS_LENGTH = -3
ERROR_EMPTY_FIELD = -4
ERROR_CANT_OPENFILE = -5
ERROR_IVALID_TAG_CONVERSION = -6

ERROR_MESSAGES = {
ERROR_CANT_OPENFILE:"Can't Open file ",
ERROR_IVALID_LINE : "Invalid Line",
ERROR_IVALID_TAG :"Invalid Tag",
ERROR_TAGS_LENGTH : "Invalid tags length",
ERROR_EMPTY_FIELD : "An Empty Field",
ERROR_IVALID_TAG_CONVERSION: "Invalid tags conversion",
}
class DataBuilder:
    def __init__(self,filename ="", sep="\t"):
        pass
        self.dic = {}
        self.lines = []
        self.data = []
        self.sep= sep
        self.TAG_SEP  = " "
        self.TAG_JOINER  = "+"
        self.FIELDS_LENGTH  = 4
        self.tags= { 0: [ "اسم", "حرف", "فعل"],
    1: [
        "جار",
        "جازم",
        "خبر",
        "زمان",
        "صفة",
        # ~ "ضمير",
        "عطف",
        "فاعل",
        "فعل",
        "مبتدأ",
        "مجرور",
        "مضاف",
        "معطوف",
        "مفعول",
        "مكان",
        "ناصب",
    ],
    2: [
        "أمر",
        "جار",
        "جازم",
        "خبر",
        "زمان",
        "صفة",
        # ~ "ضمير",
        "عطف",
        "فاعل",
        "ماضي",
        "مبتدأ",
        "مجرور",
        "مجزوم",
        "مرفوع",
        "مضارع",
        "مضاف",
        "معطوف",
        "مفعول",
        "مكان",
        "منصوب",
        "ناصب",
    ],
    3: [],
}


        self.combined_collected_tags={
    0: ["حرف+اسم", "حرف+فعل"],
    1: [
        "جار+ضمير",
        "جار+مجرور",
        "جازم+فعل",
        "عطف+جازم",
        "عطف+فعل",
        "فعل+مفعول",
        "ناصب+فعل",
    ],
    2: [
        "جار+ضمير",
        "جار+مجرور",
        "جازم+مضارع+مجزوم",
        "عطف+جازم",
        "عطف+مضارع+مرفوع",
        "مضارع+مجزوم",
        "مضارع+مجزوم+مفعول",
        "مضارع+مرفوع",
        "مضارع+منصوب",
    ],
    3: [],
}
        self.sub_tags= {"اسم":[
        # ~ "جار",
        # ~ "جازم",
        "خبر",
        "زمان",
        "صفة",
        "ضمير",
        # ~ "عطف",
        "فاعل",
        # ~ "فعل",
        "مبتدأ",
        "مجرور",
        "مضاف",
        "معطوف",
        "مفعول",
        "مكان",
        # ~ "ناصب",
        ],
         "حرف":[
        "جار",
        "جازم",
        "زمان",
        # ~ "ضمير",
        "عطف",
        "مكان",
        "ناصب",         
         ],
          "فعل":[
        "فعل",          
          ]
        }
        self.collected_tags={0:[],1:[],
        2:[],
        3:[]}        
        # ~ self.tags_small = ["vrb", "nou", "tool"]
        # ~ self.tags_medium  =['conj', 'jar', 'sbj', 'vrb', 'khbr', 'jazm', 'obj', 'conjd', 'mbtd', 'mjror', 'added', 'pplace']
        
        # ~ self.tags_small_collected = []
        # ~ self.tags_medium_collected  =[]

    def load(self, filename='', text=""):
        """ load text from file or from csv text"""
        try:
            myfile=open(filename, encoding="utf-8")

        except:
            self.log(ERROR_CANT_OPENFILE, 0, "Can't Open file %s"%filename) 
            return []
            
        else:
            lines = myfile.readlines()
            self.lines = lines
            return lines
            
    def collect_all_tags(self, lines):
        """
        Check lines validity
        """
        for ln, line in enumerate(lines):
            # lines started with # are ignored
            fields = self.extract_fields(line)
            if fields:
                # ~ fields = line.strip().split(self.sep)
                # ~ fields = [f.strip() for f in fields]
                # ~ fields = [f for f in fields if f]
                self.collect_tags(fields)
        # make uniq all collected tags
        for category in self.collected_tags:
            self.collected_tags[category] = sorted(list(set(self.collected_tags[category])))
            self.collected_tags[category] = [ x for x in self.collected_tags[category] if x] 
        for category in self.combined_collected_tags:
            self.combined_collected_tags[category] = sorted(list(set(self.combined_collected_tags[category])))
                       
    def collect_tags(self, fields):
        """
        Collect all tags in data
        """
        #if any fields is empty 
        for i, f in enumerate(fields[1:]):
            # ~ tags = f.split(" ")
            # ~ simple_tags = []
            # ~ combined_tags = []
            # ~ for tag in tags:
                # ~ if not "+" in tag:
                    # ~ simple_tags.append(tag)
                # ~ else:
                    # ~ # add combined tags into list
                    # ~ combined_tags.append(tag)
                    # ~ # add all parts of tags into simple
                    # ~ parts = tag.split("+")
                    # ~ simple_tags.extend(parts)
            tags = self.extract_tags(f)
            simple_tags = tags.get("simple",[])
            combined_tags = tags.get("combined",[])                   
            # add a key for collected tags
            if i not in self.collected_tags:
                self.collected_tags[i] = []
                self.combined_collected_tags[i] = []
            self.collected_tags[i].extend(simple_tags)
            self.combined_collected_tags[i].extend(combined_tags)

    def count_quiz_by_tags(self, lines, simple_only=False):
        """
        Count Quiz by tags.
        Simple_only: count only simple tags, used by default
        """
        collection_tags = {}
        for fields in self.data:
            # lines started with # are ignored
            # ~ fields = self.extract_fields(line)
            # ~ if fields: 
                #if any fields is empty 
            for i, f in enumerate(fields[1:]):
                tags = self.extract_tags(f)
                simple_tags = tags.get("simple",[])
                combined_tags = tags.get("combined",[]) 
                        
                # add a key for collection tags
                if i not in collection_tags:
                    collection_tags[i] = []
                # add all tags once to collection tags
                # to count quiz by tags
                collection_tags[i].extend(list(set(simple_tags)))
                # count only simple
                if not simple_only:
                    collection_tags[i].extend(list(set(combined_tags)))
        # Build counts
        counts = {i:Counter(collection_tags[i]) for i in collection_tags}
        return counts
        
    def format_counts(self, counts, output=''):
        """
        Format counts as output
        """
        if  output.lower() =="csv":
            text = "\t".join(["level", "tag", "Freq"])
            for k in counts:
                for tag in counts[k]:
                    text += "\n"+"\t".join([str(k), tag, str(counts[k][tag])])
            return text
        else:
            return counts        
        
    def extract_tags(self,field):
        """
        Extract Simple and combined tags,
        return a dict of lists.
        """
        simple_tags = []
        combined_tags = []

        tags = field.split(self.TAG_SEP)
        tags = [t for t in tags if t]
                
        for tag in tags:

            if not self.TAG_JOINER in tag:
                simple_tags.append(tag)
            else:
                # add combined tags into list
                combined_tags.append(tag)
                # add all parts of tags into simple
                parts = tag.split(self.TAG_JOINER)
                simple_tags.extend(parts)
        return {"simple": simple_tags,
            "combined":combined_tags,
        }
        
    def extract_fields(self,line):
        """
        Extract fields from line, 
        managed by number of fields 
        """
        if line.startswith("#"):
            return []
        else:
            fields  = line.strip().split(self.sep)
            fields = [f.strip() for f in fields]         
            fields = fields[:self.FIELDS_LENGTH]
        return fields
        
    def check_lines(self, lines):
        """
        Check lines validity
        """
        for ln, line in enumerate(lines):
            # lines started with # are ignored
            fields = self.extract_fields(line)
            if fields:
                result = self.check(fields)
                if result < 0:
                    # result is an error code
                    self.log(result,ln, line)                
                else:
                    self.data.append(fields)
            
             
    def check(self, fields):
        """
        Check fields in a line
        """
        #if any fields is empty 
        for f in fields:
            if not f: # empty field
                return ERROR_EMPTY_FIELD
        phrase = fields[0]

        # check all fields tags length
        for i, tags_string in enumerate(fields[1:]):
            if not self.check_length(phrase, tags_string):
                return ERROR_TAGS_LENGTH

        # check all fields tags valid
        for i, tags_string in enumerate(fields[1:]):
            if not self.check_valid_tags(tags_string, i):
                # ~ self.log(ERROR_TAGS_LENGTH, lineno,"[field %d]:%s"%(i, line))
                return ERROR_IVALID_TAG

        # check fields conversion
        if fields[1:] and len(fields)>=4:
            if not self.check_tags_conversion(fields[1:]):
               return ERROR_IVALID_TAG_CONVERSION
        return True


        
            
    def check_valid_tags(self, tag_field, category):
        """
        check if tag exist and tag_field not null and number of tags equal to words count.
        given phrase.
        given tag fields as string
        given category of tags (small, medium, large
        """
        # check for tags
        
        tags = re.split("[ \+]", tag_field)
        tags =  [t for t in tags if t]        
        for t in tags:
            if not t in self.tags[category]:
                self.log(ERROR_IVALID_TAG,0,t)
                return False
        return True

    def check_tags_conversion(self, tag_fields):
        """
        check if different tags are convertables 
        given tag fields as list of strings
        """
        # check for tags
        if len(tag_fields)<3:
            print("A field is empty") 
            return False
        basic_tags = tag_fields[0].split(" ")
        medium_tags = tag_fields[1].split(" ")
        large_tags = tag_fields[2].split(" ")
        basic_tags = [t for t in basic_tags if t]
        medium_tags = [t for t in medium_tags if t]        
        large_tags = [t for t in large_tags if t]
        if len(basic_tags)!= len(medium_tags) or len(basic_tags)!= len(large_tags) :
            
            return False
        # compare medium to basic:
        # each class must correspand to basic
        # جازم is حرف
        for b,m,l in zip(basic_tags, medium_tags, large_tags):
            if not self.check_sub_tags(b,m):
                return False
            # ~ if l not in sub_tags.get(m, []):
                # ~ return False
        return True        

    def check_sub_tags(self, tag1, tag2):
        """
        """
        # problem in combined tags, exist in one tag and not exists in he other.
        if (self.TAG_JOINER in tag1 and self.TAG_JOINER not in tag2) or (self.TAG_JOINER not in tag1 and self.TAG_JOINER in tag2):
            print("y", tag1, tag2)
            return False
        # if no combined tag
        elif self.TAG_JOINER not in tag1:
            if tag2 not in self.sub_tags.get(tag1, []):
                print("x", tag2, tag1)
                return False
        # if combined tag
        else:
            subtags1 = tag1.split(self.TAG_JOINER)
            subtags2 = tag2.split(self.TAG_JOINER)
            for st1, st2 in zip(subtags1, subtags2):
                if st2 not in self.sub_tags.get(st1, []):
                    message = "[%s][%s] sub[%s] not in [%s]"%(subtags1, subtags2, st2, st1)
                    self.log(ERROR_IVALID_TAG_CONVERSION,0,message )
                    return False
        return True
                
    def check_length(self, phrase, tag_field):
        """
        check if number of tags equal to words count.
        given phrase.
        given tag fields as string
        """
        # check for tags 
        tags = tag_field.split(" ")
        tokens = phrase.split(' ')
        tags =  [t for t in tags if t]
        tokens =  [t for t in tokens if t]
        if len(tags)!= len(tokens):
            line= "%d!=%d [%s][%s]"%(len(tokens),len(tags), tokens, tags)
            self.log(ERROR_TAGS_LENGTH,0,line )
            return False
        return True

    def build(self):
        """Build the data rows from lines"""
        dic = {"small":[], "medium":[], "large":[]}
        for fields in self.data:
            phrase = fields[0]
            words = [w for w in phrase.split(" ") if w]
            ln = len(words)
            if len(fields) >= 2 and len(words)<=4 and fields[1]:
            # ~ if len(fields) >= 2 and len(words)<=4 and fields[1]:
                dic["small"].append({"sentence":fields[0], "answer":fields[1]})
            if len(fields) >= 3 and fields[2]:
                dic["medium"].append({"sentence":fields[0], "answer":fields[2]})
            if len(fields) >= 4 and fields[3]:
                if fields[3] != fields[2]:
                    dic["large"].append({"sentence":fields[0], "answer":fields[3]})
        self.dic = dic
            
    def jsonfy(self):
        """Return jsonfy"""
        print(json.dumps(self.dic, ensure_ascii=False, indent=2))
    
    def log(self,errno, lineno, line):
        """ display errors when checkeing"""
        print("ERROR code %d:%s at line:%d\t%s"%(errno, self.get_error(errno),lineno, line))
        
    def get_error(self,errno):
        """"""
        return ERROR_MESSAGES.get(errno, "ERROR Unexpected")

        
def main(args):
    args = grabargs()
    filename = args.filename
    outfile = args.outfile
    limit = args.limit
  
    builder  = DataBuilder(sep="\t")
    lines = builder.load(filename)
    
    # test collect tags from Data
    builder.collect_all_tags(lines)
    print("Colleted Tags")
    pprint.pprint(builder.collected_tags)
    print("Combined Colleted Tags")
    pprint.pprint(builder.combined_collected_tags)
 
    
    # check valid lines
    builder.check_lines(lines)
    builder.build()
    print("-----------DATA----------")
    print(builder.data)
    print("----END-------DATA----------")   
    # ~ print(builder.dic)
    # reduce small cases:
    builder.dic["small"] = builder.dic["small"][:100]
    builder.jsonfy()
    print("Small", len(builder.dic["small"]))
    print("medium",len(builder.dic["medium"]))
    print("large", len(builder.dic["medium"]))
    print(" Counts by fields and tags")
    counts = builder.count_quiz_by_tags(lines, simple_only=True)
    print(builder.format_counts(counts, "csv"))
    print(counts)
  


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
