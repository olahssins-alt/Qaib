import re, sys
S='/tmp/claude-0/-home-user-Qaib/b14861b7-3a66-5395-ae0d-7321566137e8/scratchpad/'
shell = open(S+'pro_shell.html', encoding='utf-8').read()
main  = open(S+'pro_main.js', encoding='utf-8').read()
marker = '''  const m = new T.Mesh(geo, [face, side]);
  return m;
}
</script>'''
shell = shell.replace(marker, '''  const m = new T.Mesh(geo, [face, side]);
  return m;
}

''' + main + '\n</script>')
shell = shell.replace('__THREE__', open(S+'three.min.js', encoding='utf-8').read())
shell = shell.replace('__AUDIO__', open(S+'audio.js', encoding='utf-8').read())
shell = shell.replace('__TIMELINE__', open(S+'timeline.js', encoding='utf-8').read())
shell = shell.replace('__ART__', open(S+'art.js', encoding='utf-8').read())
open('/home/user/Qaib/QuickAIBook_ad_forge.html','w',encoding='utf-8').write(shell)
scripts = re.findall(r'<script>(.*?)</script>', shell, re.S)
open(S+'exforge.js','w',encoding='utf-8').write(scripts[1])
print('assembled', len(shell))
