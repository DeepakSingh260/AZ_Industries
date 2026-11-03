/* ═══════════════════════════════════════════════════════════════════
   AZ Industrial Solutions — Product catalogue data
   ───────────────────────────────────────────────────────────────────
   Edit this file to add or change products. No HTML changes needed.

   category  : a product catalogue. Only the first category whose status is
               'live' is shown on the site; others are kept here for later.
   family    : a group of products inside a category (e.g. "PPH Fittings")
   product   : { n, name, spec, size }
     n     : number shown on the card (matches the printed catalogue)
     name  : product name
     spec  : size text shown on the card, exactly as printed
     size  : { unit:'mm'|'in', min, max } used to build the size dropdown
             (omit it for items that are quoted without a size)
     rated : true when the item is offered in 6 kg / 10 kg pressure classes
   Images live in catalogue/img/<family id>-<nn>.jpg
   ═══════════════════════════════════════════════════════════════════ */
window.AZ_CATALOGUE = {
  /* Standard pipe outside diameters used for the size dropdown */
  sizesMM: [20,25,32,40,50,63,75,90,110,125,140,160,180,200,225,250,280,315,355,400,450,500,560,630],
  sizesIN: [{v:0.5,l:'1/2"'},{v:0.75,l:'3/4"'},{v:1,l:'1"'},{v:1.25,l:'1-1/4"'},{v:1.5,l:'1-1/2"'},{v:2,l:'2"'},{v:2.5,l:'2-1/2"'},{v:3,l:'3"'},{v:4,l:'4"'}],

  categories: [
    {
      id: 'industrial',
      name: 'Industrial',
      short: 'Equipment & industrial components',
      status: 'hidden',
      blurb: 'Our industrial equipment and component listings are being prepared. If you already know what you need, send us the details and we will quote it.'
    },
    {
      id: 'fittings',
      name: 'HDPE Fittings',
      short: 'Industrial pipe fittings · 7 families · 99 products',
      status: 'live',
      title: 'Industrial Pipe Fittings',
      intro: 'Flanges, stub ends, bends, tees, reducers, couplers, end caps and threaded adaptors in HDPE, PP, PPH, PPRC and PVDF, plus electrofusion and spigot ranges. Specify the fitting, size and quantity and we will quote pricing and availability for delivery anywhere in Canada.',
      families: [
        {
          id: 'hdpe', num: '01', name: 'HDPE Fittings',
          desc: 'Flange connections, bends, tees, reducers and end fittings.',
          products: [
            { n: 1,  name: 'Short Neck Stub End',    spec: '20-630 mm OD', size: { unit: 'mm', min: 20, max: 630 } },
            { n: 2,  name: 'Long Neck Stub End',     spec: '20-630 mm OD', size: { unit: 'mm', min: 20, max: 630 } },
            { n: 3,  name: 'Slip-on Flange',         spec: '20-630 mm OD', size: { unit: 'mm', min: 20, max: 630 } },
            { n: 4,  name: 'Blind Flange',           spec: '20-630 mm OD', size: { unit: 'mm', min: 20, max: 630 } },
            { n: 5,  name: 'Sandwich Flange',        spec: '32-315 mm OD', size: { unit: 'mm', min: 32, max: 315 } },
            { n: 6,  name: 'Paddle Flange',          spec: '75-315 mm OD', size: { unit: 'mm', min: 75, max: 315 } },
            { n: 7,  name: 'Weld Neck Flange',       spec: '75-200 mm OD', size: { unit: 'mm', min: 75, max: 200 } },
            { n: 8,  name: 'Bend (6 kg / 10 kg)',    spec: '20-160 mm OD', size: { unit: 'mm', min: 20, max: 160 }, rated: true },
            { n: 9,  name: 'Tee (6 kg / 10 kg)',     spec: '20-160 mm OD', size: { unit: 'mm', min: 20, max: 160 }, rated: true },
            { n: 10, name: 'Reducer',                spec: '32-315 mm OD', size: { unit: 'mm', min: 32, max: 315 } },
            { n: 11, name: 'End Cap',                spec: '63-450 mm OD', size: { unit: 'mm', min: 63, max: 450 } },
            { n: 12, name: 'Tail Piece',             spec: '32-160 mm OD', size: { unit: 'mm', min: 32, max: 160 } },
            { n: 13, name: 'Tail Piece with Flange', spec: '32-110 mm OD', size: { unit: 'mm', min: 32, max: 110 } }
          ]
        },
        {
          id: 'ef', num: '02', name: 'Electrofusion Fittings',
          desc: 'Connection products for polyethylene piping systems.',
          products: [
            { n: 1, name: 'Electrofusion Tee',         spec: 'Kit: 125-315 mm OD · 50-110 mm OD',  size: { unit: 'mm', min: 50, max: 315 } },
            { n: 2, name: 'Electrofusion Elbow 90°',   spec: 'Kit: 125-315 mm OD · 50-110 mm OD',  size: { unit: 'mm', min: 50, max: 315 } },
            { n: 3, name: 'Electrofusion Coupler',     spec: '20-315 mm OD',                        size: { unit: 'mm', min: 20, max: 315 } },
            { n: 4, name: 'Electrofusion End Cap',     spec: 'Kit: 125-315 mm OD · 32-110 mm OD',  size: { unit: 'mm', min: 32, max: 315 } },
            { n: 5, name: 'Electrofusion Elbow 45°',   spec: 'Kit: 125-315 mm OD · 32-110 mm OD',  size: { unit: 'mm', min: 32, max: 315 } },
            { n: 6, name: 'Stub End (180 mm Long)',    spec: '32-315 mm OD',                        size: { unit: 'mm', min: 32, max: 315 } },
            { n: 7, name: 'Electrofusion Tapping Tee', spec: '63-160 mm OD',                        size: { unit: 'mm', min: 63, max: 160 } },
            { n: 8, name: 'Electrofusion Saddle',      spec: '63-160 mm OD',                        size: { unit: 'mm', min: 63, max: 160 } },
            { n: 9, name: 'Electrofusion Reducer',     spec: 'Kit: 125-315 mm OD · 20-110 mm OD',  size: { unit: 'mm', min: 20, max: 315 } }
          ]
        },
        {
          id: 'spigot', num: '03', name: 'Spigot Fittings',
          desc: 'Spigot end caps, bends, tees, reducing tees and flanges.',
          products: [
            { n: 1, name: 'Spigot End Cap',              spec: '20-160 mm OD', size: { unit: 'mm', min: 20, max: 160 } },
            { n: 2, name: 'Bend, Spigot Type (6/10 kg)', spec: '20-315 mm OD', size: { unit: 'mm', min: 20, max: 315 }, rated: true },
            { n: 3, name: 'Tee, Spigot Type (6/10 kg)',  spec: '20-315 mm OD', size: { unit: 'mm', min: 20, max: 315 }, rated: true },
            { n: 4, name: 'Sandwich Flange',             spec: '20-315 mm OD', size: { unit: 'mm', min: 20, max: 315 } },
            { n: 5, name: 'Spigot Reducing Tee',         spec: '63-315 mm OD', size: { unit: 'mm', min: 63, max: 315 } },
            { n: 6, name: 'Spigot Elbow 45°',            spec: '20-315 mm OD', size: { unit: 'mm', min: 20, max: 315 } },
            { n: 7, name: 'Reducer, Spigot Type',        spec: '20-315 mm OD', size: { unit: 'mm', min: 20, max: 315 } }
          ]
        },
        {
          id: 'pph', num: '04', name: 'PPH Fittings',
          desc: 'Fittings for industrial piping and process applications.',
          products: [
            { n: 1,  name: 'Short Neck Stub End',               spec: '20-400 mm OD', size: { unit: 'mm', min: 20, max: 400 } },
            { n: 2,  name: 'Long Neck Stub End',                spec: '20-400 mm OD', size: { unit: 'mm', min: 20, max: 400 } },
            { n: 3,  name: 'Slip-on Flange',                    spec: '20-400 mm OD', size: { unit: 'mm', min: 20, max: 400 } },
            { n: 4,  name: 'Blind Flange',                      spec: '20-400 mm OD', size: { unit: 'mm', min: 20, max: 400 } },
            { n: 5,  name: 'Bend, Socket Weld (6/10 kg)',       spec: '20-160 mm OD', size: { unit: 'mm', min: 20, max: 160 }, rated: true },
            { n: 6,  name: 'Tee, Socket Weld (6/10 kg)',        spec: '20-160 mm OD', size: { unit: 'mm', min: 20, max: 160 }, rated: true },
            { n: 7,  name: 'Bend, Spigot Type (6/10 kg)',       spec: '63-315 mm OD', size: { unit: 'mm', min: 63, max: 315 }, rated: true },
            { n: 8,  name: 'Tee, Spigot Type (6/10 kg)',        spec: '63-315 mm OD', size: { unit: 'mm', min: 63, max: 315 }, rated: true },
            { n: 9,  name: 'Reducing Tee, Socket / Butt Weld',  spec: '32-315 mm OD', size: { unit: 'mm', min: 32, max: 315 } },
            { n: 10, name: 'Reducer, Socket / Butt Weld',       spec: '20-400 mm OD', size: { unit: 'mm', min: 20, max: 400 } },
            { n: 11, name: 'End Cap, Socket / Butt Weld',       spec: '20-400 mm OD', size: { unit: 'mm', min: 20, max: 400 } },
            { n: 12, name: 'Tail Piece',                        spec: '32-315 mm OD', size: { unit: 'mm', min: 32, max: 315 } },
            { n: 13, name: 'Core Flange',                       spec: '32-160 mm OD', size: { unit: 'mm', min: 32, max: 160 } },
            { n: 14, name: 'PPH Sandwich Flange',               spec: '20-315 mm OD', size: { unit: 'mm', min: 20, max: 315 } },
            { n: 15, name: 'PPH Coupler',                       spec: '20-160 mm OD', size: { unit: 'mm', min: 20, max: 160 } },
            { n: 16, name: 'PPH Union',                         spec: '20-63 mm OD',  size: { unit: 'mm', min: 20, max: 63 } }
          ]
        },
        {
          id: 'pprc', num: '05', name: 'PPRC Fittings',
          desc: 'Fusion fittings, threaded adapters, tees and flanged components.',
          products: [
            { n: 1,  name: 'Bend 90°',                 spec: '20-160 mm OD',    size: { unit: 'mm', min: 20, max: 160 } },
            { n: 2,  name: 'Bend 45°',                 spec: '20-160 mm OD',    size: { unit: 'mm', min: 20, max: 160 } },
            { n: 3,  name: 'Tee',                      spec: '20-160 mm OD',    size: { unit: 'mm', min: 20, max: 160 } },
            { n: 4,  name: 'Coupler',                  spec: '20-160 mm OD',    size: { unit: 'mm', min: 20, max: 160 } },
            { n: 5,  name: 'Slip-on Flange',           spec: '20-400 mm OD',    size: { unit: 'mm', min: 20, max: 400 } },
            { n: 6,  name: 'Core Flange (Long Neck)',  spec: '20-160 mm OD',    size: { unit: 'mm', min: 20, max: 160 } },
            { n: 7,  name: 'Reducer',                  spec: '20-160 mm OD',    size: { unit: 'mm', min: 20, max: 160 } },
            { n: 8,  name: 'Reducing Tee',             spec: '20-160 mm OD',    size: { unit: 'mm', min: 20, max: 160 } },
            { n: 9,  name: 'Ball Valve',               spec: '1/2 - 2 1/2 inch', size: { unit: 'in', min: 0.5, max: 2.5 } },
            { n: 10, name: 'Union',                    spec: '20-63 mm OD',     size: { unit: 'mm', min: 20, max: 63 } },
            { n: 11, name: 'End Cap',                  spec: '20-160 mm OD',    size: { unit: 'mm', min: 20, max: 160 } },
            { n: 12, name: 'MS Powder Coated Flange',  spec: '20-160 mm OD',    size: { unit: 'mm', min: 20, max: 160 } },
            { n: 13, name: 'Spigot Elbow',             spec: '63-315 mm OD',    size: { unit: 'mm', min: 63, max: 315 } },
            { n: 14, name: 'Spigot Tee',               spec: '63-315 mm OD',    size: { unit: 'mm', min: 63, max: 315 } },
            { n: 15, name: 'Long Neck',                spec: '125-400 mm OD',   size: { unit: 'mm', min: 125, max: 400 } },
            { n: 16, name: 'Welding Machine Die',      spec: '20-160 mm',       size: { unit: 'mm', min: 20, max: 160 } },
            { n: 17, name: 'Female Thread Tee',        spec: '20-32 mm OD',     size: { unit: 'mm', min: 20, max: 32 } },
            { n: 18, name: 'Male Thread Elbow',        spec: '20-32 mm OD',     size: { unit: 'mm', min: 20, max: 32 } },
            { n: 19, name: 'Female Thread Elbow',      spec: '20-32 mm OD',     size: { unit: 'mm', min: 20, max: 32 } },
            { n: 20, name: 'Male Thread Adaptor',      spec: '20-63 mm OD',     size: { unit: 'mm', min: 20, max: 63 } },
            { n: 21, name: 'Male Thread Tee',          spec: '20-32 mm OD',     size: { unit: 'mm', min: 20, max: 32 } },
            { n: 22, name: 'Female Thread Adaptor',    spec: '20-63 mm OD',     size: { unit: 'mm', min: 20, max: 63 } }
          ]
        },
        {
          id: 'pp', num: '06', name: 'PP Fittings',
          desc: 'Polypropylene fittings, including socket and threaded products.',
          products: [
            { n: 1,  name: 'Short Neck Stub End',          spec: '20-500 mm OD', size: { unit: 'mm', min: 20, max: 500 } },
            { n: 2,  name: 'Long Neck Stub End',           spec: '20-500 mm OD', size: { unit: 'mm', min: 20, max: 500 } },
            { n: 3,  name: 'Slip-on Flange',               spec: '20-630 mm OD', size: { unit: 'mm', min: 20, max: 630 } },
            { n: 4,  name: 'Blind Flange',                 spec: '20-630 mm OD', size: { unit: 'mm', min: 20, max: 630 } },
            { n: 5,  name: 'Threaded Flange',              spec: '20-315 mm OD', size: { unit: 'mm', min: 20, max: 315 } },
            { n: 6,  name: 'Bend (6 kg / 10 kg)',          spec: '20-160 mm OD', size: { unit: 'mm', min: 20, max: 160 }, rated: true },
            { n: 7,  name: 'Tee (6 kg / 10 kg)',           spec: '20-160 mm OD', size: { unit: 'mm', min: 20, max: 160 }, rated: true },
            { n: 8,  name: 'Bend, Spigot Type (6/10 kg)',  spec: '63-315 mm OD', size: { unit: 'mm', min: 63, max: 315 }, rated: true },
            { n: 9,  name: 'Tee, Spigot Type (6/10 kg)',   spec: '63-315 mm OD', size: { unit: 'mm', min: 63, max: 315 }, rated: true },
            { n: 10, name: 'Tail Piece, Flanged',          spec: '32-315 mm OD', size: { unit: 'mm', min: 32, max: 315 } },
            { n: 11, name: 'Reducer',                      spec: '20-630 mm OD', size: { unit: 'mm', min: 20, max: 630 } },
            { n: 12, name: 'End Cap',                      spec: '63-400 mm OD', size: { unit: 'mm', min: 63, max: 400 } },
            { n: 13, name: 'Tail Piece',                   spec: '32-315 mm OD', size: { unit: 'mm', min: 32, max: 315 } },
            { n: 14, name: 'Socket (Plain)',               spec: '20-200 mm OD', size: { unit: 'mm', min: 20, max: 200 } },
            { n: 15, name: 'Socket Bend (Plain)',          spec: '20-160 mm OD', size: { unit: 'mm', min: 20, max: 160 } },
            { n: 16, name: 'Socket Tee (Plain)',           spec: '20-160 mm OD', size: { unit: 'mm', min: 20, max: 160 } },
            { n: 17, name: 'Socket (Threaded)',            spec: '20-63 mm OD',  size: { unit: 'mm', min: 20, max: 63 } },
            { n: 18, name: 'Socket Bend (Threaded)',       spec: '20-63 mm OD',  size: { unit: 'mm', min: 20, max: 63 } },
            { n: 19, name: 'Socket Tee (Threaded)',        spec: '20-63 mm OD',  size: { unit: 'mm', min: 20, max: 63 } }
          ]
        },
        {
          id: 'pvdf', num: '07', name: 'PVDF Fittings',
          desc: 'PVDF connection products and fusion fittings.',
          products: [
            { n: 1,  name: 'Bend 90°',                      spec: '20-160 mm OD', size: { unit: 'mm', min: 20, max: 160 } },
            { n: 2,  name: 'Bend 45°',                      spec: '20-160 mm OD', size: { unit: 'mm', min: 20, max: 160 } },
            { n: 3,  name: 'Tee',                           spec: '20-160 mm OD', size: { unit: 'mm', min: 20, max: 160 } },
            { n: 4,  name: 'Coupler',                       spec: '20-160 mm OD', size: { unit: 'mm', min: 20, max: 160 } },
            { n: 5,  name: 'Slip-on Flange',                spec: '20-160 mm OD', size: { unit: 'mm', min: 20, max: 160 } },
            { n: 6,  name: 'Core Flange (Long Neck)',       spec: '20-160 mm OD', size: { unit: 'mm', min: 20, max: 160 } },
            { n: 7,  name: 'Reducer, Socket / Butt Weld',   spec: '20-160 mm OD', size: { unit: 'mm', min: 20, max: 160 } },
            { n: 8,  name: 'Union',                         spec: '20-63 mm',     size: { unit: 'mm', min: 20, max: 63 } },
            { n: 9,  name: 'Butt Weld Elbow',               spec: '1/2 - 1 inch', size: { unit: 'in', min: 0.5, max: 1 } },
            { n: 10, name: 'Butt Weld Tee',                 spec: '1/2 - 1 inch', size: { unit: 'in', min: 0.5, max: 1 } },
            { n: 11, name: 'Blind Flange',                  spec: '20-160 mm',    size: { unit: 'mm', min: 20, max: 160 } },
            { n: 12, name: 'End Cap, Socket / Butt Weld',   spec: '20-160 mm',    size: { unit: 'mm', min: 20, max: 160 } },
            { n: 13, name: 'Core Flange Socket',            spec: '20-160 mm OD', size: { unit: 'mm', min: 20, max: 160 } }
          ]
        }
      ]
    },
    {
      id: 'electronics',
      name: 'Electronics',
      short: 'Electronic & electrical components',
      status: 'hidden',
      blurb: 'Our electronics catalogue is being prepared. If you already know what you need, send us the details and we will quote it.'
    }
  ]
};
