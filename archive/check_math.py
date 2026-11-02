"""Reproducible algebra/numerical checks for 论文解析.md.
Run: python 验证/check_math.py (from the deliverable directory), or run by absolute path.
Symbolic identities are algebra checks, not a formal proof of the entire equilibrium.
"""
from pathlib import Path
import json
import math
import sys

import numpy as np
import sympy as s
from scipy.optimize import minimize, root_scalar
from scipy.special import lambertw, logsumexp

checks = []


def symbolic(name, expr):
    out = s.simplify(expr)
    assert out == 0, (name, out)
    checks.append({'name': name, 'kind': 'symbolic identity', 'result': 'PASS'})


def numeric(name, err, tol=1e-8):
    assert math.isfinite(float(err)) and abs(err) < tol, (name, err, tol)
    checks.append({'name': name, 'kind': 'numerical residual', 'residual': float(err), 'tolerance': tol, 'result': 'PASS'})


# Household utility derivatives.
C, N, D, sigma, eta, Om, kap, pi, lam, w, pD = s.symbols('C N D sigma eta Omega kappa pi lambda w pD', positive=True)
u = C**(1-sigma)/(1-sigma) - Om*N**(1+eta)/(1+eta) - kap*pi*D**2
symbolic('HH consumption marginal utility', s.diff(u, C)-C**(-sigma))
symbolic('HH labor FOC', (s.diff(u, N)+lam*w).subs(lam,C**(-sigma))*C**sigma - (w-Om*C**sigma*N**eta))
symbolic('HH raw data FOC', (s.diff(u,D)+lam*pD).subs(lam,C**(-sigma))*C**sigma - (pD-2*kap*pi*D*C**sigma))

# Conditional factor prices, unit cost and intermediary accounting.
A, K, n, Phi, alpha, xi, r = s.symbols('A K n Phi alpha xi r', positive=True)
T = A*Phi**(alpha*xi)*K**alpha*n**(1-alpha)
symbolic('MP capital', s.diff(T,K)-alpha*T/K)
symbolic('MP labor', s.diff(T,n)-(1-alpha)*T/n)
symbolic('MP accumulated data', s.diff(T,Phi)-alpha*xi*T/Phi)
B, g, lh, lx, ph, px = s.symbols('B gamma lh lx ph px', positive=True)
h = B*D**g*lh**(1-g)
x = B*D**g*lx**(1-g)
rev = ph*h+px*x
symbolic('Nonrival raw data value sums over destinations', D*s.diff(rev,D)-g*rev)
symbolic('Destination labor revenue shares', lh*s.diff(rev,lh)+lx*s.diff(rev,lx)-(1-g)*rev)
symbolic('Joint constant-returns accounting', D*s.diff(rev,D)+lh*s.diff(rev,lh)+lx*s.diff(rev,lx)-rev)

beta, dk, df, mc, Y, q, varphi = s.symbols('beta deltaK deltaPhi mc Y q varphi', positive=True)
rk=1/beta-1+dk
rf=1/beta-1+df
symbolic('Steady capital Euler', beta*(rk+1-dk)-1)
qsol=alpha*xi*mc*Y/(Phi*rf)
symbolic('Steady data Euler', qsol-beta*(alpha*xi*mc*Y/Phi+(1-df)*qsol))
symbolic('Steady flow spending share', (qsol*df*Phi)-df*alpha*xi*mc*Y/rf)

# Nested CES own price elasticity: d ln y / d ln p = -m+(m-rho)*share.
p, z, m, rho = s.symbols('p z m rho', positive=True)
P=(p**(1-m)+z**(1-m))**(1/(1-m))
y=(p/P)**(-m)*P**(-rho)
share=p**(1-m)/(p**(1-m)+z**(1-m))
symbolic('Nested CES own-price elasticity', -p*s.diff(s.log(y),p)-(m*(1-share)+rho*share))

# CES demand and price index, checked for substitutes and complements.
def ces_quant(logx, weights, eps):
    return math.exp(logsumexp(np.log(weights)/eps+(eps-1)/eps*np.array(logx))*eps/(eps-1))

ces_rows=[]
for eps in [.01,.5,2.,5.,10.]:
    weights=np.array([.4,.6]); prices=np.array([1.3,2.1]); Q=2.7
    logP=logsumexp(np.log(weights)+(1-eps)*np.log(prices))/(1-eps)
    Pval=math.exp(logP)
    quantities=weights*(prices/Pval)**(-eps)*Q
    numeric(f'CES primal, omega={eps}', ces_quant(np.log(quantities),weights,eps)-Q)
    numeric(f'CES expenditure identity, omega={eps}', prices@quantities-Pval*Q)
    numeric(f'CES FOC ratio, omega={eps}', (weights[0]/weights[1])**(1/eps)*(quantities[0]/quantities[1])**(-1/eps)-prices[0]/prices[1])
    ces_rows.append({'omega':eps,'price_index':Pval,'domestic':quantities[0],'foreign':quantities[1]})
# Normalized omega -> 1 CES limit, which is not the unnormalized Cobb-Douglas.
weights=np.array([.4,.6]); amounts=np.array([2.,3.])
cd=np.prod((amounts/weights)**weights)
numeric('Normalized Cobb-Douglas limit omega=1+1e-5', ces_quant(np.log(amounts),weights,1+1e-5)-cd,tol=2e-6)

# A closed steady state constructed analytically and verified against every load-bearing FOC.
pars=dict(beta=.99,sigma=2.,eta=1.3,Omega=1.315,alpha=1/3,deltaK=.025,deltaPhi=.025,rho=21.,xi=1.,gamma=.5,B=1.,A=1.,kappa=1.,pi=1.)
b,sg,et,O,a,dkv,dfv,rhov,xiv,gv,Bv,Av,kv,piv=[pars[k] for k in ['beta','sigma','eta','Omega','alpha','deltaK','deltaPhi','rho','xi','gamma','B','A','kappa','pi']]
muinv=(rhov-1)/rhov; rkval=1/b-1+dkv; rfval=1/b-1+dfv
kY=a*muinv/rkval
cY=1-dkv*kY
sphi=a*xiv*dfv/rfval
ellshare=(1-gv)*sphi/((1-a)+(1-gv)*sphi)
aN=muinv*((1-a)+(1-gv)*sphi)/(O*cY**sg)
aD=gv*sphi*muinv/(2*kv*piv*cY**sg)
h_exp=1-a+(1-gv)*a*xiv
E=1-a-(1-sg)*(gv*a*xiv/2+h_exp/(1+et))
logH=(math.log(Av)+a*math.log(kY)+a*xiv*math.log(Bv/dfv)
      +gv*a*xiv/2*math.log(aD)+(1-gv)*a*xiv*math.log(ellshare)
      +(1-a)*math.log(1-ellshare)+h_exp/(1+et)*math.log(aN))
yv=math.exp(logH/E)
cv=cY*yv; Kv=kY*yv; Nv=(aN*yv**(1-sg))**(1/(1+et)); Dv=math.sqrt(aD*yv**(1-sg))
lv=ellshare*Nv; nv=(1-ellshare)*Nv; fv=Bv*Dv**gv*lv**(1-gv); Pv=fv/dfv
wv=O*cv**sg*Nv**et; qv=sphi*muinv*yv/fv; pdv=gv*qv*fv/Dv
numeric('Closed SS goods production', Av*Pv**(a*xiv)*Kv**a*nv**(1-a)-yv)
numeric('Closed SS goods resource', cv+dkv*Kv-yv)
numeric('Closed SS capital demand', rkval*Kv-a*muinv*yv)
numeric('Closed SS production labor', wv*nv-(1-a)*muinv*yv)
numeric('Closed SS data-sector labor', wv*lv-(1-gv)*qv*fv)
numeric('Closed SS raw data demand', pdv*Dv-gv*qv*fv)
numeric('Closed SS household raw data supply', pdv-2*kv*piv*Dv*cv**sg)
numeric('Closed SS data Euler', qv-b*(a*xiv*muinv*yv/Pv+(1-dfv)*qv))
numeric('Closed SS data intermediary zero profit', qv*fv-pdv*Dv-wv*lv)
numeric('Closed SS household budget including firm profits', cv+dkv*Kv-(wv*Nv+rkval*Kv+pdv*Dv+(1-muinv)*yv-qv*fv))
closed=dict(Y=yv,C=cv,K=Kv,N=Nv,n=nv,l=lv,D=Dv,varphi=fv,Phi=Pv,w=wv,q=qv,PD=pdv,exponent=E)

# Distinguish stationary FOC roots from finite dynamic profit maximization.
# Closed-economy operating profits after optimizing k,n,y scale as Phi**theta.
price_elasticity = rhov
revenue_exponent = (price_elasticity-1)/price_elasticity
data_exponent = a*xiv
unit_cost_without_data = (rkval/a)**a*(wv/(1-a))**(1-a)/Av
aggregate_demand_scale = yv**(1/price_elasticity)

def operating_profit(data_stock):
    output = (revenue_exponent*aggregate_demand_scale/unit_cost_without_data)**price_elasticity*data_stock**(data_exponent*price_elasticity)
    revenue = aggregate_demand_scale*output**revenue_exponent
    marginal_cost = unit_cost_without_data*data_stock**(-data_exponent)
    return revenue-marginal_cost*output, output, marginal_cost

profit0, output0, cost0 = operating_profit(Pv)
profit1, output1, cost1 = operating_profit(2*Pv)
numeric('Conditional operating output optimum', revenue_exponent*aggregate_demand_scale*output1**(-1/price_elasticity)-cost1)
numeric('Operating profit data-scale exponent (not an optimum certificate)', profit1/profit0-2**(data_exponent*(price_elasticity-1)))

# Welfare CEV algebra and new export-safeguard extension.
Ualt, V0, W0, C0, bpar = s.symbols('Ualt V0 W0 C0 b', real=True)
# (1+g)^(1-sigma) = [(1-sigma)(V_alt+W0)]/C0^(1-sigma).
cev_power=(1-sigma)*(Ualt+W0)/C0**(1-sigma)
symbolic('Steady CEV utility equality', cev_power*C0**(1-sigma)/(1-sigma)-W0-Ualt)
D1, x1, e1, k1, b1, ss, he, vH, vF = s.symbols('D x e k b s he vH vF', positive=True)
G=(vH+vF*x1)*D1-k1*D1**2*(1+b1*x1**2*s.exp(-ss*e1))-he*e1**2/2
Dstar=(vH+vF*x1)/(2*k1*(1+b1*x1**2*s.exp(-ss*e1)))
symbolic('Extension A optimal D conditional on x,e', s.diff(G,D1).subs(D1,Dstar))
symbolic('Extension A reduced value', G.subs(D1,Dstar)-((vH+vF*x1)**2/(4*k1*(1+b1*x1**2*s.exp(-ss*e1)))-he*e1**2/2))
ke,bv,sv,hev,Dc,xc=.7,1.2,1.5,.4,1.1,.6
eopt=float(lambertw(ke*bv*sv**2*Dc**2*xc**2/hev).real/sv)
numeric('Extension A Lambert W security choice', ke*bv*sv*Dc**2*xc**2*math.exp(-sv*eopt)-hev*eopt)

# Extension B bounded productivity and complementarity.
Z, M, zeta, kk, mm = s.symbols('Z M zeta k m0',positive=True)
logprod=zeta*Z/(kk+Z)*M/(mm+M)
symbolic('Extension B data marginal log productivity', s.diff(logprod,Z)-zeta*kk/(kk+Z)**2*M/(mm+M))
symbolic('Extension B compute marginal log productivity', s.diff(logprod,M)-zeta*Z/(kk+Z)*mm/(mm+M)**2)
symbolic('Extension B data-compute log complementarity', s.diff(logprod,Z,M)-zeta*kk*mm/((kk+Z)**2*(mm+M)**2))

# Extension C data used both in production and capability formation.
zH, R, hh, aa, v = s.symbols('zetaH R h a v',positive=True)
innovation=zH*R**aa*Phi**(1-aa)
symbolic('Extension C MP R', s.diff(innovation,R)-zH*aa*R**(aa-1)*Phi**(1-aa))
symbolic('Extension C extra data return', s.diff(innovation,Phi)-zH*(1-aa)*R**aa*Phi**(-aa))
# Test the conditional R rule numerically without symbolic fractional-power branch assumptions.
avec=.4; zv=.3; vv=2.; phiv=5.
Rstar=(zv*avec*vv)**(1/(1-avec))*phiv
numeric('Extension C optimal training R', vv*zv*avec*Rstar**(avec-1)*phiv**(1-avec)-1)

report={
    'scope': 'Symbolic algebra identities, CES primal/dual residuals, one closed-economy steady state, and conditional extension FOCs. No open-economy IRF replication and no Lean proof are asserted.',
    'python':sys.version.split()[0], 'sympy':s.__version__,
    'checks':checks,'number_of_checks':len(checks),
    'closed_economy_parameters':pars,'closed_economy_steady_state':closed,
    'finite_optimum_diagnostic': {'theta':data_exponent*(price_elasticity-1), 'meaning':'Under unrestricted individual linear-price data procurement, theta>1 yields unbounded profits. The reported steady state is an FOC candidate, not a global equilibrium certificate.'},
    'CES_cases':ces_rows,'security_example_e_star':eopt,
}
out=Path(__file__).with_name('检查结果.json')
out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'{len(checks)} checks PASS')
print(json.dumps(closed,indent=2))
print('Report:',out)
