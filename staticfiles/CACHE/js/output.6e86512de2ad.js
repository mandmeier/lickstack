const chords_dir="/static/img/chords/";const tortoise_on_url="/static/img/tortoise_hover.webp";const tortoise_off_url="/static/img/tortoise_toggled.webp";;function canUseWebP(){var elem=document.createElement('canvas');if(!!(elem.getContext&&elem.getContext('2d'))){return elem.toDataURL('image/webp').indexOf('data:image/webp')==0;}
return false;}
function img_ext(){if(canUseWebP()){return".webp";}return".png";}
function transposeChord(input,transpose_by){element=input.match(/(_[a-gA-g]{1,2}_)/)[0]
if(transpose_by>=0){var chds=["_C_","_Db_","_D_","_Eb_","_E_","_F_","_Gb_","_G_","_Ab_","_A_","_Bb_","_B_"]}else{var chds=["_C_","_B_","_Bb_","_A_","_Ab_","_G_","_Gb_","_F_","_E_","_Eb_","_D_","_Db_"]}
var start=chds.indexOf(element)
element_transposed=chds[(start+Math.abs(transpose_by))%chds.length];return input.replace(/(_[a-gA-g]{1,2}_)/,element_transposed);}
function transposePlayer(l){transpose_bys[l]=Number(licks[l].getElementsByClassName('transpose-btn')[0].value)
playback_rates[l]=licks[l].getElementsByClassName('slowdown-btn')[0].value
audios[l].playbackRate=playback_rates[l];players[l].playbackRate=playback_rates[l];players[l].toDestination();for(let j=0;j<pitch_shifts.length;j++){if(pitch_shifts[j]!=null){pitch_shifts[j].disconnect();}
delete pitch_shifts[j]}
if(playback_rates[l]==1){pitch_shifts[l]=new Tone.PitchShift({pitch:transpose_bys[l].toString()}).toDestination();}else{trans=transpose_bys[l]+12
trans=trans.toString()
pitch_shifts[l]=new Tone.PitchShift({pitch:trans}).toDestination();}
players[l].disconnect();players[l].connect(pitch_shifts[l]);}
function updateChords(lick_id){l=lick_order.indexOf(lick_id)
let lick=licks[l]
let chords=lick.getElementsByClassName('chord_seq')[0].getAttribute("value").split('x').slice(1,17);let transpose_rules=lick.getElementsByClassName('transpose_rule')[0].getAttribute('value').split(',')
let transpose=Number(lick.getElementsByClassName('transpose-btn')[0].value)
let chord_imgs=lick.getElementsByTagName('img')
let i
for(i=0;i<16;i++){if(!chord_imgs[i].hasAttribute("name")){chord_imgs[i].name=chords[i]}
if(chords[i]=='.'){if(chord_imgs[i].src.endsWith('#')){chord_imgs[i].src=chords_dir+transpose_rules[i]+'/dash'+img_ext()}}else{chord_imgs[i].src=chords_dir+transpose_rules[i]+'/'+transposeChord(chords[i],transpose)+img_ext()}}
transposePlayer(l);}
function make_ts34(lck){let chord_fields=lck.getElementsByClassName('chord-img')
chord_fields[3].style.display="none"
chord_fields[7].style.display="none"
chord_fields[11].style.display="none"
chord_fields[15].style.display="none"
sep34=Array.prototype.slice.call(lck.getElementsByClassName('separator-34'));sep34.forEach(function(element){element.style.width='2.9%';});seplr=Array.prototype.slice.call(lck.getElementsByClassName('separator-lr'));seplr.forEach(function(element){element.style.width='5%';});sepmid=Array.prototype.slice.call(lck.getElementsByClassName('separator-mid'));sepmid.forEach(function(element){element.style.width='8.8%';});}
const licks=document.getElementsByClassName('lick')
const lick_order=[]
for(const lick of licks){lick_order.push(lick.id.split('_')[1])}
const play_btns=document.getElementsByClassName('play')
const seekBars=document.getElementsByClassName('seek-bar')
const fillBars=document.getElementsByClassName('fill')
mouseDown=false;players=[]
audios=[]
playButtonIcons=[]
playback_rates=[]
transpose_bys=[]
pitch_shifts=[]
for(let i=0;i<play_btns.length;i++){let time_signature=licks[i].getElementsByClassName('time_signature')[0].getAttribute('value');if(time_signature==34){make_ts34(licks[i]);};let audio_url=play_btns[i].id.split('[X]')[1]
players.push(new Tone.Player(audio_url));audios.push(new Audio(audio_url));playButtonIcons.push(play_btns[i].querySelector('span'));audios[i].volume=0;playback_rates.push(Number(licks[i].getElementsByClassName('transpose-btn')[0].value))
transpose_bys.push(licks[i].getElementsByClassName('slowdown-btn')[0].value)
pitch_shifts.push(null)
var start_time=0
var current_time=0
play_btns[i].addEventListener('click',function(){if(pitch_shifts[i]==undefined){transposePlayer(i);}
if(audios[i].paused){audios[i].play();ofs=audios[i].currentTime;players[i].start();players[i].seek(offset=ofs);}else{audios[i].pause();players[i].stop(0);}});audios[i].addEventListener('play',function(){playButtonIcons[i].className='icon icon-pause';resetAudio(i);});audios[i].addEventListener('pause',function(){playButtonIcons[i].className='icon icon-play';});audios[i].addEventListener('timeupdate',function(){if(mouseDown)return;let p=audios[i].currentTime/audios[i].duration;let x=fillBars[i].style.width=p*100+"%";});seekBars[i].addEventListener('mousedown',function(e){mouseDown=true;window.rect=e.target.getBoundingClientRect();let x=e.clientX-rect.left;let p=x/seekBars[i].clientWidth;fillBars[i].style.width=p*100+"%";});licks[i].addEventListener('mousemove',function(e){if(!mouseDown)return;let x=e.clientX-rect.left;let p=x/seekBars[i].clientWidth;fillBars[i].style.width=p*100+"%";});licks[i].addEventListener('mouseup',function(e){if(!mouseDown)return;mouseDown=false;let x=e.clientX-rect.left;let p=x/seekBars[i].clientWidth;fillBars[i].style.width=p*100+"%";audios[i].currentTime=p*audios[i].duration;ofs=audios[i].currentTime;if(!audios[i].paused){players[i].start();players[i].seek(offset=ofs);}});updateChords(lick_order[i]);}
function resetAudio(num){for(let i=0;i<play_btns.length;i++){if(num!=i){audios[i].pause();audios[i].currentTime=0;players[i].stop(0);}}}
function slowdown(lick_id){selected_tortoise=document.getElementById('slowdown_'+lick_id)
if(selected_tortoise.value=="1"){selected_tortoise.src=tortoise_on_url;selected_tortoise.value="0.5";}else{selected_tortoise.value="1";selected_tortoise.src=tortoise_off_url;selected_tortoise.value="1";}
transposePlayer(lick_order.indexOf(lick_id));};