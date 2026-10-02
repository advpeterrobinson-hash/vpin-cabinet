// Bilingual UTF-8 CSV from typed Artifact Tool cells. CERN-OHL-S-2.0.
// Run with the provided runtime dependency tree; no repo-local dependencies.
import fs from 'node:fs/promises';
import path from 'node:path';
import {Workbook} from '@oai/artifact-tool';
const root=process.cwd(),out=path.join(root,'exports/generated/hardware-v33');
const bom=JSON.parse(await fs.readFile(path.join(out,'bom.json'),'utf8'));
const columns=['row_id','bom_layer','description_en','description_pt_BR','quantity','quantity_status','unit','material','nominal_dimensions','status','flatpack_classification','measurement_required','assembly_stage','source','notes','notes_pt_BR','price_BRL'];
const rows=bom.rows.map(r=>columns.map(k=>typeof r[k]==='object' && r[k]!==null?JSON.stringify(r[k]):r[k]??null));
const w=Workbook.create();const s=w.worksheets.add('BOM');
s.showGridLines=false;s.getRangeByIndexes(0,0,rows.length+1,columns.length).values=[columns,...rows];
s.freezePanes.freezeRows(1);s.freezePanes.freezeColumns(1);
const range=s.getRangeByIndexes(0,0,rows.length+1,columns.length);
range.format.font={name:'Arial',size:10};range.format.rowHeight=26;
s.getRange('A1:Q1').format.fill='#233746';s.getRange('A1:Q1').format.font={color:'#FFFFFF',bold:true};
s.getRange('A1:B246').format.columnWidth=12;s.getRange('C1:D246').format.columnWidth=52;s.getRange('E1:E246').format.columnWidth=10;s.getRange('F1:F246').format.columnWidth=42;
s.getRange('F1:F246').format.wrapText=true;range.format.verticalAlignment='center';
s.getRange('C1:D246').format.wrapText=true;s.getRange('A1:Q246').format.rowHeight=42;
w.recalculate();
const exported=range.values;
if(exported.length!==rows.length+1)throw Error('CSV row mismatch');
for(let i=0;i<rows.length;i++)for(let j=0;j<columns.length;j++){
 if(JSON.stringify(exported[i+1][j]??null)!==JSON.stringify(rows[i][j]??null))throw Error(`Cell mismatch ${i},${j}`);
}
const quote=v=>v===null||v===undefined?'':`"${String(v).replaceAll('"','""')}"`;
await fs.writeFile(path.join(out,'bom.csv'),'\uFEFF'+exported.map(r=>r.map(quote).join(',')).join('\r\n')+'\r\n');
const preview=await w.render({sheetName:'BOM',range:'A1:F12',scale:1,format:'png'});
await fs.writeFile(path.join(out,'bom-preview.png'),new Uint8Array(await preview.arrayBuffer()));
await fs.writeFile(path.join(out,'csv-validation.json'),JSON.stringify({pass:true,row_count:rows.length,columns,typed_quantity_roundtrip:true,prices_unknown:true,format:'UTF-8 BOM, RFC4180 quoting, CRLF; blank quantity means unresolved, see quantity_status'},null,2)+'\n');
console.log('HARDWARE_V33_CSV_PASS',rows.length);
