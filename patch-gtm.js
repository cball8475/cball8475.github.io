const fs = require('fs');
const gtm = `
  <!-- Google Tag Manager -->
  <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
  new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  })(window,document,'script','dataLayer','GTM-ND932PHQ');</script>
  <!-- End Google Tag Manager -->`;
const files = [
  'about.html','bishopville-sc-dumpster-rental.html','chesterfield-sc-dumpster-rental.html',
  'construction-dumpster-rental-florence-sc.html','contact.html','darlington-county-landfill-guide.html',
  'darlington-sc-dumpster-rental.html','dillon-sc-dumpster-rental.html','dumpster-rental-florence-sc.html',
  'florence-sc-landfill-guide.html','hartsville-sc-dumpster-rental.html','kingstree-sc-dumpster-rental.html',
  'lake-city-sc-dumpster-rental.html','latta-sc-dumpster-rental.html','marion-sc-dumpster-rental.html',
  'mullins-sc-dumpster-rental.html','partners.html','pricing.html','privacy.html',
  'residential-dumpster-rental-darlington-hartsville.html','service-area.html','services.html',
  'sumter-sc-dumpster-rental.html','sumter-sc-landfill-guide.html','terms.html'
];
let ok = 0, skip = 0;
files.forEach(f => {
  try {
    let h = fs.readFileSync(f, 'utf8');
    if (h.includes('GTM-ND932PHQ')) { console.log('SKIP: ' + f); skip++; return; }
    h = h.replace(/<head>/i, '<head>' + gtm);
    fs.writeFileSync(f, h);
    console.log('PATCHED: ' + f);
    ok++;
  } catch (e) { console.log('ERROR: ' + f + ' - ' + e.message); }
});
console.log('\nDone: ' + ok + ' patched, ' + skip + ' skipped');
