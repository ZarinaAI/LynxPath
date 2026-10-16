const pptxgen = require('pptxgenjs');
const pptx = new pptxgen();
pptx.layout = 'LAYOUT_WIDE';
pptx.author = 'LynxPath contributors';
pptx.subject = 'LynxPath v0.1 FOSDEM demo pitch';
pptx.title = 'LynxPath v0.1 — FOSDEM Demo Pitch';
pptx.company = 'LynxPath';
pptx.lang = 'en-US';
pptx.theme = { headFontFace: 'Arial', bodyFontFace: 'Arial', lang: 'en-US' };

const C = {
  navy:'103844', navy2:'173F4A', teal:'0BA3A3', tealDark:'087B7B', tealLight:'E7F6F6',
  green:'159A6D', greenLight:'EAF7F2', orange:'F07C45', orangeLight:'FFF2EA',
  red:'D95D5D', redLight:'FCEEEE', blue:'4C7ED6', blueLight:'EDF3FF',
  ink:'16333C', text:'36515A', muted:'70828A', line:'D7E1E5', white:'FFFFFF', bg:'F5F8FA'
};

pptx.defineSlideMaster({
  title:'MASTER',
  background:{color:C.bg},
  objects:[
    {rect:{x:0,y:0,w:13.333,h:0.06,fill:{color:C.teal},line:{color:C.teal}}},
    {text:{text:'LynxPath v0.1',options:{x:0.45,y:7.10,w:2.2,h:0.2,fontFace:'Arial',fontSize:7.5,color:'71818A',margin:0}}},
    {text:{text:'Synthetic data • not for clinical use',options:{x:8.7,y:7.10,w:4.0,h:0.2,fontFace:'Arial',fontSize:7.5,color:'9AA8AF',align:'right',margin:0}}},
  ],
  slideNumber:{x:12.78,y:7.08,w:0.25,h:0.2,color:'9AA8AF',fontFace:'Arial',fontSize:7.5}
});

function title(slide,t,sub=''){
  slide.addText(t,{x:0.55,y:0.34,w:12.1,h:0.5,fontSize:24,bold:true,color:C.ink,margin:0});
  if(sub) slide.addText(sub,{x:0.55,y:0.90,w:12.1,h:0.38,fontSize:10.5,color:C.muted,margin:0});
}
function card(slide,x,y,w,h,fill=C.white,line=C.line){
  slide.addShape(pptx.ShapeType.roundRect,{x,y,w,h,fill:{color:fill},line:{color:line,width:1},radius:0.06});
}
function pill(slide,text,x,y,w,fill,color,border=fill){
  slide.addShape(pptx.ShapeType.roundRect,{x,y,w,h:0.34,fill:{color:fill},line:{color:border,width:0.8},radius:0.08});
  slide.addText(text,{x:x+0.06,y:y+0.085,w:w-0.12,h:0.14,fontSize:8.3,bold:true,color,align:'center',margin:0});
}
function line(slide,x1,y1,x2,y2,color=C.line,width=1.3){
  slide.addShape(pptx.ShapeType.line,{x:x1,y:y1,w:x2-x1,h:y2-y1,line:{color,width,beginArrowType:'none',endArrowType:'none'}});
}
function cross(slide,x,y,size=0.48,bg=C.teal){
  slide.addShape(pptx.ShapeType.ellipse,{x,y,w:size,h:size,fill:{color:bg},line:{color:bg}});
  slide.addShape(pptx.ShapeType.rect,{x:x+size*0.42,y:y+size*0.18,w:size*0.16,h:size*0.64,fill:{color:C.white},line:{color:C.white}});
  slide.addShape(pptx.ShapeType.rect,{x:x+size*0.18,y:y+size*0.42,w:size*0.64,h:size*0.16,fill:{color:C.white},line:{color:C.white}});
}
function rankRow(slide,rank,name,time,x,y,w,accent,tag=''){
  slide.addShape(pptx.ShapeType.ellipse,{x,y:y+0.02,w:0.38,h:0.38,fill:{color:accent},line:{color:accent}});
  slide.addText(String(rank),{x,y:y+0.12,w:0.38,h:0.11,fontSize:8,bold:true,color:C.white,align:'center',margin:0});
  slide.addText(name,{x:x+0.55,y,w:w-2.0,h:0.24,fontSize:11,bold:true,color:C.ink,margin:0});
  if(tag) pill(slide,tag,x+0.55,y+0.30,1.38,C.greenLight,C.green,'BCE2D2');
  slide.addText(time,{x:x+w-1.05,y:y+0.01,w:0.92,h:0.28,fontSize:14,bold:true,color:accent,align:'right',margin:0});
}
function arrow(slide,x,y,w=0.45,h=0.62,color='A8BBC1'){
  slide.addShape(pptx.ShapeType.chevron,{x,y,w,h,fill:{color},line:{color}});
}

// 1 — hero
{
  const s=pptx.addSlide('MASTER');
  s.background={color:C.navy};
  s.addShape(pptx.ShapeType.rect,{x:0,y:0,w:13.333,h:7.5,fill:{color:C.navy},line:{color:C.navy}});
  s.addShape(pptx.ShapeType.rect,{x:0,y:0,w:13.333,h:0.08,fill:{color:C.teal},line:{color:C.teal}});
  cross(s,0.72,0.72,0.58,C.teal);
  s.addText('LynxPath v0.1',{x:0.72,y:1.48,w:6.1,h:0.62,fontSize:30,bold:true,color:C.white,margin:0});
  s.addText('Open capacity signals for explainable time-to-care',{x:0.72,y:2.18,w:6.3,h:0.52,fontSize:19,color:'B9D7DD',margin:0});
  s.addText('A reproducible FOSS demo: schema → eligibility → estimator → ranked options.',{x:0.72,y:2.88,w:6.2,h:0.44,fontSize:11.2,color:'8EB8C0',margin:0});
  card(s,7.45,1.05,4.95,4.85,'154751','2A5A63');
  s.addText('Nearest ≠ fastest to care',{x:7.82,y:1.38,w:4.15,h:0.34,fontSize:15,bold:true,color:C.white,margin:0});
  pill(s,'NEAREST',7.82,2.06,1.08,'2B5963','DDECEF','2B5963');
  s.addText('Hospital A',{x:7.82,y:2.52,w:1.55,h:0.24,fontSize:11,bold:true,color:C.white,margin:0});
  s.addText('8 min travel',{x:7.82,y:2.87,w:1.55,h:0.22,fontSize:9,color:'B7CED3',margin:0});
  s.addText('186 min',{x:10.35,y:2.50,w:1.35,h:0.42,fontSize:23,bold:true,color:'FFB69A',align:'right',margin:0});
  s.addText('expected TTC',{x:10.40,y:2.93,w:1.28,h:0.20,fontSize:8.4,color:'B7CED3',align:'right',margin:0});
  line(s,7.82,3.46,12.0,3.46,'3A6870',1);
  pill(s,'FASTEST NOW',7.82,3.78,1.38,'1D765F','E7FFF4','1D765F');
  s.addText('Hospital B',{x:7.82,y:4.26,w:1.55,h:0.24,fontSize:11,bold:true,color:C.white,margin:0});
  s.addText('18 min travel',{x:7.82,y:4.61,w:1.55,h:0.22,fontSize:9,color:'B7CED3',margin:0});
  s.addText('53 min',{x:10.35,y:4.24,w:1.35,h:0.42,fontSize:23,bold:true,color:'8BE3C0',align:'right',margin:0});
  s.addText('45–61 min range',{x:10.12,y:4.70,w:1.56,h:0.20,fontSize:8.4,color:'B7CED3',align:'right',margin:0});
  s.addText('Synthetic fracture pathway: X-ray + orthopaedics',{x:7.82,y:5.31,w:4.0,h:0.24,fontSize:8.7,color:'93BCC4',margin:0});
  pill(s,'APACHE-2.0',0.72,6.08,1.22,'1A5360','C8E4E8','316873');
  pill(s,'DOCKER COMPOSE',2.08,6.08,1.50,'1A5360','C8E4E8','316873');
  pill(s,'CI + TESTS',3.73,6.08,1.12,'1A5360','C8E4E8','316873');
  pill(s,'REPRODUCIBLE SCENARIOS',5.00,6.08,2.05,'1A5360','C8E4E8','316873');
  s.addText('FOSDEM 2027 demo pitch',{x:9.85,y:6.13,w:2.55,h:0.22,fontSize:9,color:'789EA6',align:'right',margin:0});
}

// 2 — problem / model
{
  const s=pptx.addSlide('MASTER');
  title(s,'The demo asks one operational question','Required capabilities are declared first; LynxPath never infers diagnosis.');
  card(s,0.65,1.55,3.05,4.70,C.white,C.line);
  s.addText('Input',{x:0.98,y:1.92,w:1.0,h:0.27,fontSize:15,bold:true,color:C.ink,margin:0});
  s.addText('Patient pathway requirement',{x:0.98,y:2.43,w:2.2,h:0.22,fontSize:9.2,color:C.muted,margin:0});
  pill(s,'X-RAY',0.98,2.83,0.88,C.blueLight,C.blue,'C9D9F5');
  pill(s,'ORTHOPAEDICS',1.98,2.83,1.36,C.tealLight,C.tealDark,'B7DFDF');
  s.addText('The user/pathway declares these capabilities. No clinical prediction is performed.',{x:0.98,y:3.46,w:2.25,h:0.82,fontSize:10.3,color:C.text,margin:0});
  s.addText('Safety boundary',{x:0.98,y:4.72,w:1.4,h:0.22,fontSize:9.3,bold:true,color:C.orange,margin:0});
  s.addText('Information only • human decision remains final',{x:0.98,y:5.08,w:2.28,h:0.54,fontSize:10.5,bold:true,color:C.ink,margin:0});
  arrow(s,4.13,3.10,0.62,1.0,C.orange);
  card(s,5.15,1.55,7.45,4.70,C.tealLight,'B8E0E0');
  s.addText('Estimate',{x:5.50,y:1.92,w:1.2,h:0.27,fontSize:15,bold:true,color:C.ink,margin:0});
  s.addText('Expected time-to-care',{x:5.50,y:2.42,w:3.2,h:0.30,fontSize:16,bold:true,color:C.tealDark,margin:0});
  const terms=[['Travel','18 min',C.blue],['ED delay','15 min',C.orange],['X-ray delay','15 min',C.red],['Orthopaedics delay','5 min',C.green]];
  terms.forEach((r,i)=>{
    const yy=3.03+i*0.60;
    s.addText(r[0],{x:5.55,y:yy,w:2.3,h:0.22,fontSize:10,color:C.text,margin:0});
    s.addText(r[1],{x:8.33,y:yy,w:0.9,h:0.22,fontSize:10,bold:true,color:C.ink,align:'right',margin:0});
    s.addShape(pptx.ShapeType.rect,{x:5.55,y:yy+0.28,w:3.72,h:0.09,fill:{color:'DDE9EC'},line:{color:'DDE9EC'}});
    const m=parseInt(r[1]);
    s.addShape(pptx.ShapeType.rect,{x:5.55,y:yy+0.28,w:3.72*Math.min(1,m/60),h:0.09,fill:{color:r[2]},line:{color:r[2]}});
  });
  card(s,9.72,2.45,2.25,2.96,C.white,'B7DCDC');
  s.addText('53 min',{x:9.95,y:3.08,w:1.80,h:0.52,fontSize:28,bold:true,color:C.green,align:'center',margin:0});
  s.addText('expected TTC',{x:10.03,y:3.73,w:1.65,h:0.28,fontSize:10,color:C.muted,align:'center',margin:0});
  pill(s,'45–61 min',10.11,4.42,1.52,C.greenLight,C.green,'BFE2D3');
  s.addText('Freshness: 7 min • confidence: 84%',{x:9.87,y:5.02,w:1.95,h:0.30,fontSize:8.3,color:C.muted,align:'center',margin:0});
}

// 3 — open schema
{
  const s=pptx.addSlide('MASTER');
  title(s,'The technical contribution is an open capacity-signal interface','Adapters stay at the edge; the estimator consumes one small, testable representation.');
  const blocks=[
    {x:0.65,w:2.15,t:'Source feeds',sub:'FHIR-like • ROR-style • local systems • synthetic',fill:C.blueLight,border:'C8D8F5'},
    {x:3.18,w:2.55,t:'Open capacity schema',sub:'capabilities • delays • closures • source • freshness • confidence',fill:C.tealLight,border:'B6E0E0'},
    {x:6.12,w:2.35,t:'Reference engine',sub:'eligibility • TTC estimate • uncertainty',fill:C.orangeLight,border:'F1C9B5'},
    {x:8.86,w:3.80,t:'Explainable output',sub:'ranked eligible options • ranges • change reasons',fill:C.greenLight,border:'BDE1D2'}
  ];
  blocks.forEach((b,i)=>{
    card(s,b.x,2.05,b.w,2.55,b.fill,b.border);
    s.addText(b.t,{x:b.x+0.22,y:2.44,w:b.w-0.44,h:0.32,fontSize:14,bold:true,color:C.ink,align:'center',margin:0});
    s.addText(b.sub,{x:b.x+0.22,y:3.15,w:b.w-0.44,h:0.78,fontSize:9.8,color:C.text,align:'center',valign:'mid',margin:0});
    if(i<blocks.length-1) arrow(s,b.x+b.w+0.16,2.93,0.40,0.72,'AABBC1');
  });
  card(s,1.10,5.12,11.05,1.10,C.navy,'214A54');
  s.addText('New country or hospital? Write an adapter — not a new ranking engine.',{x:1.43,y:5.43,w:10.42,h:0.34,fontSize:16,bold:true,color:C.white,align:'center',margin:0});
  s.addText('The schema is versioned JSON Schema 2020-12 and the demo fixtures validate offline in CI.',{x:1.43,y:5.87,w:10.42,h:0.24,fontSize:9.6,color:'BBD8DE',align:'center',margin:0});
}

// 4 — schema snapshot
{
  const s=pptx.addSlide('MASTER');
  title(s,'A capacity snapshot is small enough to inspect','The v0.1 schema contains operational signals — no patient identifier, diagnosis, or destination decision.');
  card(s,0.65,1.55,7.05,4.95,'132F38','274953');
  const code = [
    '{',
    '  "patient_need": {',
    '    "required_capabilities": ["xray", "orthopedics"]',
    '  },',
    '  "hospitals": [{',
    '    "hospital_id": "B",',
    '    "travel_minutes": 18,',
    '    "ed_delay_minutes": 15,',
    '    "resource_delays": {"xray": 15, "orthopedics": 5},',
    '    "temporary_closures": [],',
    '    "freshness_minutes": 7,',
    '    "confidence": 0.84,',
    '    "source": "synthetic://hospital-b"',
    '  }]',
    '}'
  ].join('\n');
  s.addText(code,{x:0.98,y:1.88,w:6.35,h:4.25,fontFace:'Courier New',fontSize:10.2,color:'DDECEF',margin:0.02,breakLine:false});
  const notes=[
    ['Capabilities','Eligibility before ranking'],
    ['Operational delays','Separate ED and resource signals'],
    ['Closures','A resource can become unavailable'],
    ['Freshness','Stale data widens uncertainty'],
    ['Confidence','Visible instead of hidden'],
    ['Source','Every signal is attributable']
  ];
  notes.forEach((n,i)=>{
    const y=1.67+i*0.79;
    card(s,8.10,y,4.45,0.62,i===3?C.orangeLight:C.white,i===3?'F3C6AF':C.line);
    s.addText(n[0],{x:8.34,y:y+0.12,w:1.35,h:0.20,fontSize:10.5,bold:true,color:i===3?C.orange:C.ink,margin:0});
    s.addText(n[1],{x:9.72,y:y+0.12,w:2.46,h:0.27,fontSize:9.2,color:C.text,margin:0});
  });
}

// 5 — deterministic demo switch
{
  const s=pptx.addSlide('MASTER');
  title(s,'The live demo is deterministic: one click, a visible ranking change','Same pathway. Same hospitals. Only the operational signals change.');
  s.addText('T = 0',{x:0.78,y:1.53,w:1.1,h:0.26,fontSize:14,bold:true,color:C.ink,margin:0});
  card(s,0.67,1.92,5.48,3.76,C.white,C.line);
  rankRow(s,1,'Hospital B','53 min',0.98,2.34,4.78,C.green,'FASTEST');
  rankRow(s,2,'Hospital C','64 min',0.98,3.20,4.78,C.blue);
  rankRow(s,3,'Hospital A','186 min',0.98,4.06,4.78,C.orange);
  pill(s,'Hospital D excluded',0.98,5.04,1.68,C.redLight,C.red,'F1CACA');
  arrow(s,6.43,3.00,0.68,1.05,C.teal);
  s.addText('Next →',{x:6.31,y:4.13,w:0.93,h:0.22,fontSize:9,bold:true,color:C.tealDark,align:'center',margin:0});
  s.addText('T = 15 min',{x:7.48,y:1.53,w:1.5,h:0.26,fontSize:14,bold:true,color:C.ink,margin:0});
  card(s,7.37,1.92,5.28,3.76,C.tealLight,'B5DEDE');
  rankRow(s,1,'Hospital C','48 min',7.68,2.34,4.60,C.green,'NEW FASTEST');
  rankRow(s,2,'Hospital B','62 min',7.68,3.20,4.60,C.blue);
  rankRow(s,3,'Hospital A','187 min',7.68,4.06,4.60,C.orange);
  pill(s,'Hospital D excluded',7.68,5.04,1.68,C.redLight,C.red,'F1CACA');
  card(s,0.67,6.00,11.98,0.70,C.navy,'214A54');
  s.addText('Why it changed: Hospital C improved by 16 min; Hospital B worsened by 9 min as ED load rose.',{x:0.98,y:6.22,w:11.34,h:0.25,fontSize:10.4,bold:true,color:C.white,align:'center',margin:0});
}

// 6 — explainability / uncertainty
{
  const s=pptx.addSlide('MASTER');
  title(s,'Ranges, freshness and reasons — not a magic score','The demo makes uncertainty inspectable and widens intervals when signals are less reliable or stale.');
  card(s,0.65,1.55,5.30,4.85,C.white,C.line);
  s.addText('Hospital C at T = 15',{x:0.98,y:1.93,w:2.6,h:0.28,fontSize:15,bold:true,color:C.ink,margin:0});
  s.addText('48 min',{x:0.98,y:2.52,w:2.10,h:0.55,fontSize:31,bold:true,color:C.green,margin:0});
  s.addText('expected time-to-care',{x:0.98,y:3.05,w:2.2,h:0.24,fontSize:9.7,color:C.muted,margin:0});
  pill(s,'43–53 min range',0.98,3.55,1.58,C.greenLight,C.green,'BCE2D1');
  pill(s,'2 min old',2.72,3.55,1.10,C.tealLight,C.tealDark,'B6E0E0');
  pill(s,'91% confidence',3.98,3.55,1.35,C.blueLight,C.blue,'C8D8F5');
  line(s,0.98,4.26,5.62,4.26,'DDE6E8',1);
  const comps=[['Travel',27,C.blue],['ED delay',8,C.orange],['X-ray',8,C.red],['Orthopaedics',5,C.green]];
  comps.forEach((r,i)=>{
    const y=4.58+i*0.38;
    s.addText(r[0],{x:0.98,y,w:1.40,h:0.20,fontSize:9.3,color:C.text,margin:0});
    s.addShape(pptx.ShapeType.rect,{x:2.25,y:y+0.05,w:2.45,h:0.10,fill:{color:'E9EFF1'},line:{color:'E9EFF1'}});
    s.addShape(pptx.ShapeType.rect,{x:2.25,y:y+0.05,w:2.45*(r[1]/30),h:0.10,fill:{color:r[2]},line:{color:r[2]}});
    s.addText(`${r[1]} min`,{x:4.82,y,w:0.62,h:0.20,fontSize:9.3,bold:true,color:C.ink,align:'right',margin:0});
  });
  s.addText('The ranking explanation is generated from the same component deltas used by the estimator.',{x:6.45,y:1.76,w:5.55,h:0.56,fontSize:15,bold:true,color:C.ink,margin:0});
  const bullets=[
    ['Eligibility first','Missing or closed capabilities are excluded before ranking.'],
    ['No false precision','The UI shows a range, not only a point estimate.'],
    ['Freshness is data','Older signals increase the uncertainty margin.'],
    ['Change is explicit','The app names which delays improved or worsened.']
  ];
  bullets.forEach((b,i)=>{
    const y=2.65+i*0.86;
    s.addShape(pptx.ShapeType.ellipse,{x:6.48,y:y+0.03,w:0.25,h:0.25,fill:{color:C.teal},line:{color:C.teal}});
    s.addText('✓',{x:6.48,y:y+0.06,w:0.25,h:0.11,fontSize:8.5,bold:true,color:C.white,align:'center',margin:0});
    s.addText(b[0],{x:6.88,y,w:1.85,h:0.22,fontSize:10.8,bold:true,color:C.ink,margin:0});
    s.addText(b[1],{x:8.62,y,w:3.62,h:0.42,fontSize:9.3,color:C.text,margin:0});
  });
}

// 7 — repository / reproducibility
{
  const s=pptx.addSlide('MASTER');
  title(s,'v0.1 is built to be reproduced and extended','A FOSDEM demo should be clonable, testable and hackable — not only presented.');
  card(s,0.65,1.55,4.18,4.85,'132F38','274953');
  s.addText('Run it',{x:0.98,y:1.93,w:1.2,h:0.28,fontSize:15,bold:true,color:C.white,margin:0});
  s.addText('$ git clone …\n$ cd LynxPath\n$ docker compose up --build',{x:0.98,y:2.50,w:3.35,h:1.10,fontFace:'Courier New',fontSize:12.4,color:'DDECEF',margin:0.02});
  s.addText('Then open',{x:0.98,y:3.93,w:1.0,h:0.22,fontSize:9.5,color:'9DBBC1',margin:0});
  s.addText('http://localhost:8501',{x:0.98,y:4.32,w:2.55,h:0.28,fontFace:'Courier New',fontSize:11.5,bold:true,color:'8BE3C0',margin:0});
  pill(s,'APACHE-2.0',0.98,5.15,1.20,'1B505B','C7E3E7','326A75');
  pill(s,'GITHUB ACTIONS',2.34,5.15,1.43,'1B505B','C7E3E7','326A75');
  pill(s,'5 TESTS PASS',0.98,5.67,1.28,'1B505B','C7E3E7','326A75');
  pill(s,'3 SCENARIOS',2.42,5.67,1.20,'1B505B','C7E3E7','326A75');

  const items=[
    ['schema/','Versioned JSON Schema for capacity snapshots'],
    ['scenarios/','Deterministic fracture, stroke and trauma timelines'],
    ['lynxpath/','Eligibility, TTC estimate, uncertainty, change explanation'],
    ['tests/','Regression tests for rankings, closures and schema validation'],
    ['docs/','Demo script + ready-to-open good-first issues']
  ];
  items.forEach((it,i)=>{
    const y=1.69+i*0.88;
    card(s,5.25,y,7.35,0.70,i===0?C.tealLight:C.white,i===0?'B7E0E0':C.line);
    s.addText(it[0],{x:5.52,y:y+0.15,w:1.55,h:0.22,fontFace:'Courier New',fontSize:10.5,bold:true,color:i===0?C.tealDark:C.ink,margin:0});
    s.addText(it[1],{x:7.12,y:y+0.14,w:5.05,h:0.34,fontSize:9.3,color:C.text,margin:0});
  });
}

// 8 — community ask
{
  const s=pptx.addSlide('MASTER');
  s.background={color:C.navy};
  s.addShape(pptx.ShapeType.rect,{x:0,y:0,w:13.333,h:7.5,fill:{color:C.navy},line:{color:C.navy}});
  s.addShape(pptx.ShapeType.rect,{x:0,y:0,w:13.333,h:0.08,fill:{color:C.teal},line:{color:C.teal}});
  cross(s,0.72,0.66,0.50,C.teal);
  s.addText('Help make the capacity schema useful beyond the demo',{x:0.72,y:1.45,w:10.8,h:0.65,fontSize:27,bold:true,color:C.white,margin:0});
  s.addText('The best next contributions are concrete and independent.',{x:0.72,y:2.18,w:7.1,h:0.38,fontSize:12,color:'A9C8CE',margin:0});
  const asks=[
    ['1','Review the schema','Would these signals map cleanly from your hospital, public-sector or research system?'],
    ['2','Write an adapter','Translate an example FHIR/ROR-style/local payload into the v0.1 snapshot.'],
    ['3','Add a scenario','Contribute a reproducible bottleneck or temporary-closure case — synthetic data only.']
  ];
  asks.forEach((a,i)=>{
    const y=3.05+i*0.93;
    s.addShape(pptx.ShapeType.ellipse,{x:0.82,y:y+0.03,w:0.38,h:0.38,fill:{color:C.teal},line:{color:C.teal}});
    s.addText(a[0],{x:0.82,y:y+0.12,w:0.38,h:0.11,fontSize:8,bold:true,color:C.white,align:'center',margin:0});
    s.addText(a[1],{x:1.45,y,w:2.15,h:0.25,fontSize:13,bold:true,color:C.white,margin:0});
    s.addText(a[2],{x:3.68,y,w:7.75,h:0.42,fontSize:10,color:'B7D3D9',margin:0});
  });
  card(s,0.72,6.18,11.92,0.72,'154751','2B5A64');
  s.addText('Open schema • explainable estimator • reproducible scenarios • Apache-2.0',{x:1.00,y:6.41,w:11.35,h:0.25,fontSize:11,bold:true,color:'D5EBEE',align:'center',margin:0});
}

pptx.writeFile({ fileName: 'docs/LynxPath_v0.1_FOSDEM_Demo_Pitch.pptx' });
