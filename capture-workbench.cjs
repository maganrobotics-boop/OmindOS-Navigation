const {chromium}=require('playwright');
const fs=require('fs');
(async()=>{
fs.mkdirSync('capture-output',{recursive:true});
const browser=await chromium.launch({headless:true});
const page=await browser.newPage({viewport:{width:1500,height:1060},deviceScaleFactor:1});
const errors=[];page.on('pageerror',e=>errors.push(e.message));
for(let i=0;i<30;i++){try{await page.goto('http://127.0.0.1:8085/',{waitUntil:'networkidle',timeout:10000});break;}catch(e){if(i===29)throw e;await new Promise(r=>setTimeout(r,500));}}
await page.locator('#example').click();
await page.waitForFunction(()=>document.querySelector('#model-info').textContent.includes('12'));
await page.locator('#fit').click();
await page.waitForTimeout(1000);
await page.screenshot({path:'capture-output/quadruped-workbench.png'});
await page.locator('#part').selectOption({label:'fl_thigh'}).catch(()=>{});
await page.locator('#editor').screenshot({path:'capture-output/parameter-editor.png'});
const report={source:'public preview.6 Linux x64 binary',package_sha256:'134fc899a9c2f320527578d8eb80e88ffabb4d44e4e87942828edc0351b79bfe',title:await page.title(),info:await page.locator('#model-info').innerText(),page_errors:errors};
fs.writeFileSync('capture-output/CAPTURE.json',JSON.stringify(report,null,2)+'\n');
if(errors.length)throw Error(JSON.stringify(errors));
console.log(JSON.stringify(report));
await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
