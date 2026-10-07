(function(){
  // Dropdowns + mobile menu
  const head=document.querySelector('.site-head');
  const drops=[...document.querySelectorAll('.nav .has-sub')];
  function closeAll(except){drops.forEach(d=>{if(d!==except){d.classList.remove('open');d.querySelector('button').setAttribute('aria-expanded','false');d.querySelector('.sub').hidden=true}})}
  drops.forEach(d=>{
    const b=d.querySelector('button'),s=d.querySelector('.sub');
    b.addEventListener('click',e=>{e.stopPropagation();const open=s.hidden;closeAll(d);s.hidden=!open;d.classList.toggle('open',open);b.setAttribute('aria-expanded',String(open))});
  });
  document.addEventListener('click',e=>{if(!e.target.closest('.nav'))closeAll()});
  const burger=document.querySelector('.burger');
  if(burger)burger.addEventListener('click',()=>{const on=head.classList.toggle('menu');burger.setAttribute('aria-expanded',String(on))});

  const still=matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Hero slideshow
  const hero=document.querySelector('.hero');
  if(hero){
    const slides=[...hero.querySelectorAll('img')];let i=0,t;
    const go=n=>{slides[i].classList.remove('on');i=(n+slides.length)%slides.length;slides[i].classList.add('on')};
    const run=()=>{clearInterval(t);if(!still)t=setInterval(()=>go(i+1),5500)};
    hero.querySelector('.prev').addEventListener('click',()=>{go(i-1);run()});
    hero.querySelector('.next').addEventListener('click',()=>{go(i+1);run()});
    run();
  }

  // Card carousel
  document.querySelectorAll('.carousel').forEach(c=>{
    const tr=c.querySelector('.track'),p=c.querySelector('.prev'),n=c.querySelector('.next');
    const step=()=>tr.querySelector('.card').getBoundingClientRect().width+parseFloat(getComputedStyle(tr).columnGap||0);
    const upd=()=>{p.disabled=tr.scrollLeft<4;n.disabled=tr.scrollLeft+tr.clientWidth>=tr.scrollWidth-4};
    p.addEventListener('click',()=>tr.scrollBy({left:-step(),behavior:still?'auto':'smooth'}));
    n.addEventListener('click',()=>tr.scrollBy({left:step(),behavior:still?'auto':'smooth'}));
    tr.addEventListener('scroll',upd,{passive:true});addEventListener('resize',upd);upd();
  });

  // Lightbox
  const shots=[...document.querySelectorAll('[data-full]')];
  if(shots.length){
    const lb=document.createElement('div');lb.className='lb';lb.hidden=true;lb.setAttribute('role','dialog');lb.setAttribute('aria-label','Photo viewer');
    const ic=d=>`<svg viewBox="0 0 24 24" stroke-width="1"><path d="${d}"/></svg>`;
    lb.innerHTML=`<img alt=""><button class="x" aria-label="Close">${ic('M5 5l14 14M19 5L5 19')}</button><button class="l" aria-label="Previous photo">${ic('M15 4l-8 8 8 8')}</button><button class="r" aria-label="Next photo">${ic('M9 4l8 8-8 8')}</button>`;
    document.body.appendChild(lb);
    const im=lb.querySelector('img');let k=0;
    const show=n=>{k=(n+shots.length)%shots.length;im.src=shots[k].dataset.full;im.alt=shots[k].querySelector('img')?.alt||''};
    const close=()=>{lb.hidden=true;shots[k].focus()};
    shots.forEach((s,n)=>s.addEventListener('click',()=>{show(n);lb.hidden=false;lb.querySelector('.x').focus()}));
    lb.querySelector('.x').addEventListener('click',close);
    lb.querySelector('.l').addEventListener('click',()=>show(k-1));
    lb.querySelector('.r').addEventListener('click',()=>show(k+1));
    lb.addEventListener('click',e=>{if(e.target===lb)close()});
    addEventListener('keydown',e=>{if(lb.hidden)return;if(e.key==='Escape')close();if(e.key==='ArrowLeft')show(k-1);if(e.key==='ArrowRight')show(k+1)});
  }
})();

(function(){
  const f=document.getElementById('contact-form');if(!f)return;
  const st=document.getElementById('contact-status'),b=f.querySelector('button');
  f.addEventListener('submit',async e=>{
    e.preventDefault();b.disabled=true;st.textContent='Sending…';
    try{
      const r=await fetch(f.action,{method:'POST',headers:{'Accept':'application/json'},body:new FormData(f)});
      const d=await r.json();
      if(r.ok&&d.success){f.reset();st.textContent='Thank you — your message has been sent.'}
      else{st.textContent='Sorry, the message could not be sent. Please try again later.'}
    }catch(_){st.textContent='Sorry, the message could not be sent. Please try again later.'}
    b.disabled=false;
  });
})();
