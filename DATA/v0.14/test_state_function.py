import ctypes as c, subprocess, numpy as np, json, csv
from pathlib import Path
p=Path('/mnt/data'); src=p/'NeuroCore_Autonomous_014/neurocore.c'; so=p/'nc_state_test.so'
subprocess.run(['gcc','-std=c11','-O2','-shared','-fPIC',str(src),'-lm','-o',str(so)],check=True)
class NC(c.Structure):
 _fields_=[('z',c.c_float*8),('velocity',c.c_float*8),('anchors',(c.c_float*8)*4),('count',c.c_float*4),('residual_ema',c.c_float),('confidence',c.c_float),('last_novelty',c.c_float),('innovation_ema',c.c_float),('persistence',c.c_float),('directional',c.c_float*8),('directional_energy',c.c_float),('initialized',c.c_int),('used',c.c_int),('last_match',c.c_int),('stable_count',c.c_int)]
lib=c.CDLL(str(so));lib.nc_init.argtypes=[c.POINTER(NC)];lib.nc_step.argtypes=[c.POINTER(NC),c.POINTER(c.c_float),c.c_int,c.POINTER(c.c_float)]
rows=[]; traces=[]
for case in ['impulse','persistent','return']:
 for seed in range(60):
  rng=np.random.default_rng(80000+seed); n=400; truth=np.zeros(n)
  if case=='impulse': truth[:]=0.35
  if case=='persistent':truth[:200]=0.35;truth[200:]=0.85
  if case=='return':truth[:120]=0.35;truth[120:260]=0.85;truth[260:]=0.35
  obs=truth+rng.normal(0,.035,n)
  if case=='impulse':obs[200:204]+=1.3
  s=NC();lib.nc_init(c.byref(s)); out=(c.c_float*5)(); pred=[]; conf=[]; used=[]; match=[]
  for x in obs:
   arr=(c.c_float*1)(float(x));lib.nc_step(c.byref(s),arr,1,out)
   pred.append(float(out[0]));conf.append(float(out[3]));used.append(int(out[4]));match.append(int(out[2]))
  pred=np.array(pred); ema=np.empty(n);ema[0]=obs[0]
  for i in range(1,n):ema[i]=ema[i-1]+.19*(obs[i]-ema[i-1])
  for method,y in [('NC',pred),('EMA019',ema)]:
   rows.append(dict(case=case,seed=seed,method=method,rmse=float(np.sqrt(np.mean((y-truth)**2))),pre_rmse=float(np.sqrt(np.mean((y[80:190]-truth[80:190])**2))),event_error=float(np.mean(np.abs(y[200:204]-truth[200:204]))) if case=='impulse' else float(np.mean(np.abs(y[210:240]-truth[210:240]))),return_error=float(np.mean(np.abs(y[275:310]-truth[275:310]))) if case=='return' else None))
  if seed==0:traces.append(dict(case=case,anchors=used[-1],matched_samples=sum(m>=0 for m in match),at_199=pred[199],at_203=pred[203],at_239=pred[239],at_279=pred[279],at_399=pred[399]))
with open(p/'state_function_results.csv','w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
summary={case:{method:{key:round(float(np.mean([r[key] for r in rows if r['case']==case and r['method']==method and r[key] is not None])),5) for key in ['rmse','event_error','return_error'] if any(r['case']==case and r['method']==method and r[key] is not None for r in rows)} for method in ['NC','EMA019']} for case in ['impulse','persistent','return']}
print(json.dumps({'summary':summary,'traces':traces},indent=2))
(p/'state_function_summary.json').write_text(json.dumps({'summary':summary,'traces':traces,'protocol':'60 independent noise seeds per scenario, one channel, 400 samples, 0.035 Gaussian observation noise; impulse four samples amplitude 1.3; step and return amplitude 0.5; EMA gain 0.19; synthetic exploratory test'},indent=2))
