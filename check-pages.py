"""Browser checks for the static frontend. Requires optional Playwright and Chromium."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import os
base=os.environ.get('PREVIEW_BASE_URL','http://127.0.0.1:8000')
pages=['index.html','company-application.html','service-application.html','cooperation-application.html','activity-application.html','research-application.html','consultation-application.html','applications.html','ru.html','uz.html']
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1440,'height':1000});errors=[]
 page.on('pageerror',lambda err:errors.append(str(err)))
 for file in pages:
  response=page.goto(base+'/'+file);assert response.status==200,file
  page.locator('h1').wait_for();assert page.locator('#site-header a').count()>0,file
  assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),file
 page.goto(base+'/index.html');page.screenshot(path='preview-desktop.png',full_page=True)
 page.locator('[data-guide=税务]').click();page.get_by_role('dialog').wait_for();page.get_by_role('link',name='提交相关咨询').click()
 assert page.locator('#f-guide').input_value()=='税务'
 # Each of six forms can save a validated record and query it after reload.
 for kind in ['company','service','cooperation','activity','research','consultation']:
  page.goto(base+'/'+kind+'-application.html')
  form=page.locator('#application-form')
  for element in form.locator('input[required],textarea[required],select[required]').all():
   tag=element.evaluate('(el)=>el.tagName');type_=element.get_attribute('type')
   if tag=='SELECT':element.select_option(index=1)
   elif type_=='checkbox':element.check()
   elif type_=='number':element.fill('2')
   else:element.fill('测试资料-'+(element.get_attribute('name')or''))
  form.locator('[type=submit]').click();page.get_by_role('dialog').wait_for()
  # Repeating the submission keeps the same record, including after closing modal.
  before=page.evaluate('JSON.parse(localStorage.getItem("chamber-static-applications-v1")).length')
  page.locator('[data-close]').first.click();form.locator('[type=submit]').click();page.get_by_role('dialog').wait_for()
  assert page.evaluate('JSON.parse(localStorage.getItem("chamber-static-applications-v1")).length')==before
  page.get_by_role('link',name='查看我的申请').click();page.locator('[data-close]').first.click();page.reload()
  page.locator('#application-list article').first.wait_for()
  if page.locator('[data-close]').count():page.locator('[data-close]').first.click()
 assert page.locator('#application-list article').count()==6
 page.locator('#kind-filter').select_option('service');assert page.locator('#application-list article').count()==1
 page.get_by_role('link',name='修改资料').click();page.locator('#f-title').fill('<script>alert(1)</script>');page.locator('[type=submit]').click();page.locator('[data-close]').first.click()
 page.goto(base+'/applications.html');page.get_by_role('heading',name='<script>alert(1)</script>',exact=True).wait_for()
 page.once('dialog',lambda dialog:dialog.accept());page.locator('[data-withdraw]').first.click();assert page.locator('#application-list').inner_text().count('企业撤回')==1
 # Draft restoration and attachment limits.
 page.goto(base+'/service-application.html');page.locator('#f-company').fill('草稿企业');page.locator('[data-draft]').click();page.reload();assert page.locator('#f-company').input_value()=='草稿企业'
 page.locator('#attachments').set_input_files({'name':'script.html','mimeType':'text/html','buffer':b'test'});assert '仅支持' in page.locator('#file-feedback').inner_text()
 # Storage failure retains form values and gives a visible error.
 page.locator('#attachments').set_input_files([])
 page.evaluate("() => { Storage.prototype.setItem=function(){throw new DOMException('storage unavailable','QuotaExceededError')}; }")
 page.locator('[data-draft]').click();assert page.locator('#f-company').input_value()=='草稿企业';assert '存储不可用' in page.locator('#toast').inner_text()
 page.goto(base+'/consultation-application.html?lang=ru');assert page.locator('html').get_attribute('lang')=='ru';assert 'Компания' in page.locator('form').inner_text();assert '保存演示' not in page.locator('form').inner_text()
 page.locator('#language-select').select_option('uz');assert page.locator('html').get_attribute('lang')=='uz';assert 'Hamkorlik' in page.locator('h1').inner_text()
 mobile=browser.new_page(viewport={'width':390,'height':844},is_mobile=True,has_touch=True);mobile.on('pageerror',lambda err:errors.append(str(err)))
 for file in pages:
  mobile.goto(base+'/'+file);mobile.locator('h1').wait_for();assert mobile.evaluate('document.documentElement.scrollWidth <= innerWidth'),file
 mobile.goto(base+'/index.html');mobile.screenshot(path='preview-mobile.png',full_page=True)
 for private in ['/.git/config','/package.json','/check-pages.py','/node_modules/tailwindcss/package.json','/%2e%2e/README.md']:
  assert page.request.get(base+private).status==404,private
 assert not errors,errors
 browser.close()
 print('PASS: 10 desktop/mobile pages; six forms; duplicate prevention; reload/search/edit/withdraw; draft; attachment rejection; storage failure; RU/UZ consultation; preview private-file blocking.')
