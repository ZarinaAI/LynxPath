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
