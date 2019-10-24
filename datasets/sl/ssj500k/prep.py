import xml.etree.ElementTree as ET
import random
random.seed(42)
def next_sent():
  conllu=open('ssj500k.conllu/ssj500k-ud-morphology.conllu')
  sent=[]
  for line in conllu:
    if not line.startswith('#'):
      if line.strip()=='':
        yield sent
        sent=[]
      else:
        line=line.split('\t')
        sent.append([line[3],line[5]])
get_next_sent=next_sent()
get_next_sent=next_sent()
tree=ET.parse('ssj500k-en.TEI/ssj500k-en.body.xml')
root=tree.getroot()
train=[]
dev=[]
test=[]
train_jos=[]
dev_jos=[]
test_jos=[]
train_ud=[]
dev_ud=[]
test_ud=[]
train_text=open('train.txt','w')
dev_text=open('dev.txt','w')
test_text=open('test.txt','w')
train_jos_text=open('train_jos.txt','w')
dev_jos_text=open('dev_jos.txt','w')
test_jos_text=open('test_jos.txt','w')
train_ud_text=open('train_ud.txt','w')
dev_ud_text=open('dev_ud.txt','w')
test_ud_text=open('test_ud.txt','w')
for doc in root.iter('{http://www.tei-c.org/ns/1.0}div'):
  rand=random.random()
  if rand<0.8:
    pointer=train
    pointer_text=train_text
    pointer_ud=train_ud
    pointer_ud_text=train_ud_text
    pointer_jos=train_jos
    pointer_jos_text=train_jos_text
  elif rand<0.9:
    pointer=dev
    pointer_text=dev_text
    pointer_ud=dev_ud
    pointer_ud_text=dev_ud_text
    pointer_jos=dev_jos
    pointer_jos_text=dev_jos_text    
  else:
    pointer=test
    pointer_text=test_text
    pointer_ud=test_ud
    pointer_ud_text=test_ud_text
    pointer_jos=test_jos
    pointer_jos_text=test_jos_text
  for p in doc.iter('{http://www.tei-c.org/ns/1.0}p'):
    for element in p:
      if element.tag.endswith('s'):
        sentence=element
        text=''
        tokens=[]
        uposfeats=get_next_sent.next()
        jos=None
        ud=None
        for element in sentence:
          if element.tag[-3:]=='seg':
            for subelement in element:
              text+=subelement.text
              if not subelement.tag.endswith('}c'):
                if subelement.tag.endswith('w'):
                  lemma=subelement.attrib['lemma']
                else:
                  lemma=subelement.text
                tokens.append([subelement.text,lemma,subelement.attrib['ana'].split(':')[1]])
          if element.tag[-2:] not in ('pc','}w','}c'):
            if element.tag[-7:]=='linkGrp':
              if element.attrib['type']=='UD-SYN':
                ud=[]
                for subelement in element:
                  label=subelement.attrib['ana'].split(':')[1]
                  head,dep=subelement.attrib['target'].split(' ')
                  head=head.split('.')[-1]
                  if head[0]!='t':
                    head='0'
                  else:
                    head=head[1:]
                  ud.append((head,label))
              elif element.attrib['type']=='JOS-SYN':
                jos=[]
                for subelement in element:
                  label=subelement.attrib['ana'].split(':')[1]
                  head,dep=subelement.attrib['target'].split(' ')
                  head=head.split('.')[-1]
                  if head[0]!='t':
                    head='0'
                  else:
                    head=head[1:]
                  jos.append((head,label))
            continue
          text+=element.text
          if not element.tag.endswith('}c'):
            if element.tag.endswith('w'):
              lemma=element.attrib['lemma']
            else:
              lemma=element.text
            tokens.append([element.text,lemma,element.attrib['ana'].split(':')[1]])
        tokens=[a+b for a,b in zip(tokens,uposfeats)]
        pointer.append((text,tokens))
        pointer_text.write(text.encode('utf8'))
        if ud!=None:
          pointer_ud.append((text,tokens,ud))
          pointer_ud_text.write(text.encode('utf8'))
        if jos!=None:
          pointer_jos.append((text,tokens,jos))
          pointer_jos_text.write(text.encode('utf8'))
      else:
        pointer_text.write(element.text.encode('utf8'))
        if ud!=None:
          pointer_ud_text.write(element.text.encode('utf8'))
        if jos!=None:
          pointer_jos_text.write(element.text.encode('utf8'))
    pointer_text.write('\n')
    if ud!=None:
      pointer_ud_text.write('\n')
    if jos!=None:
      pointer_jos_text.write('\n')
  #pointer_text.write('\n')

def write_list(lst,fname,synt=False):
  f=open(fname,'w')
  for el in lst:
    if not synt:
      text,tokens=el
    else:
      text,tokens,dep=el
    f.write('# text = '+text.encode('utf8')+'\n')
    for idx,token in enumerate(tokens):
      if synt==False:
        f.write(str(idx+1)+'\t'+token[0].encode('utf8')+'\t'+token[1].encode('utf8')+'\t'+token[3]+'\t'+token[2]+'\t'+token[4]+'\t_\t_\t_\t_\n')
      else:
        f.write(str(idx+1)+'\t'+token[0].encode('utf8')+'\t'+token[1].encode('utf8')+'\t'+token[3]+'\t'+token[2]+'\t'+token[4]+'\t'+dep[idx][0].encode('utf8')+'\t'+dep[idx][1].encode('utf8')+'\t_\t_\n')
    f.write('\n')
  f.close()

write_list(train,'train.conllu')
write_list(dev,'dev.conllu')
write_list(test,'test.conllu')
write_list(train_jos,'train_jos.conllu',True)
write_list(dev_jos,'dev_jos.conllu',True)
write_list(test_jos,'test_jos.conllu',True)
write_list(train_ud,'train_ud.conllu',True)
write_list(dev_ud,'dev_ud.conllu',True)
write_list(test_ud,'test_ud.conllu',True)
train_text.close()
dev_text.close()
test_text.close()
train_ud_text.close()
dev_ud_text.close()
test_ud_text.close()
train_jos_text.close()
dev_jos_text.close()
test_jos_text.close()
