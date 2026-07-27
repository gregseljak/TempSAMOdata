#%%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
pd.set_option("display.max_colwidth", None)
infile=os.path.expanduser("~")\
    +"/thesis/predoc3/samo_diplomacy/samo_mse_private.csv"
df=pd.read_csv(infile)

def contruct_plname(indict):
    name=f"{indict['TestFunction']}-{indict['dim']}"
    thetaname=""
    if "Lat" in indict["DrawMethod"]:
        if "Rp" in indict["DrawMethod"]:
            thetaname="Lat-Rpv-"
        elif "Rv" in indict["DrawMethod"]:
            thetaname="Lat-Rv-"
        else:
            thetaname="Lat-"
        if indict["shift"]=="rqmc":
            thetaname+="RS"

    if "Sob" in indict["DrawMethod"]:
        if "NUS" in indict["DrawMethod"]:
            thetaname="Sob-NUS-"
        elif "LMS" in indict["DrawMethod"]:
            thetaname="Sob-LMS-"
        else:
            thetaname="Sob-"
        if indict["shift"]=="rqmc":
            thetaname+="RDS"
    if indict["baker"]:
        thetaname+="B"
    if not thetaname.endswith("-"):
        thetaname=thetaname+"-"
    return f"{name}-{thetaname}{indict['log2n']}-10000.dat"
df["datfile"] = df.apply(contruct_plname, axis=1)
df11=df[df["rDrawn"]==11]
duplicates = df11[df11["datfile"].duplicated(keep=False)]
duplicates
del df11
# %%
FpRQMC=["Lat","Sob","Sob-NUS"]
RpRQMC=["Lat-Rp","Sob-LMS"]

df=df[~(df["TestFunction"]=="RidgeJohnsonSU")]
### Do stuff to df


#df[(df["TestFunction"]=="MC2")&(df["dim"]==32)&(df["DrawMethod"]=="Sob-LMS")&(df["log2n"]==12)]
# %%

df["ratio"]=df["MeanOfMeans"]/df["MedianOfMeans"]
df["dotsize"]=np.abs(np.log(\
    df["MeanOfMeans"]/df["MedianOfMeans"])\
    )*3
df["dotcolor"] = np.where(df["ratio"] > 1,
    "C1", "C2")
cauchschwartz_skew=10**np.linspace(\
    np.min(np.log10(np.abs(df["skew"]/10))),
    np.max(np.log10(np.abs(df["skew"]*10))),
    1000)
cauchyschwartz_kurt=1+cauchschwartz_skew**2

fig,ax=plt.subplots(ncols=3,
    sharex=True,sharey=True,
    figsize=(10,3))

fprqmc_df=df[(df["DrawMethod"].isin(FpRQMC))&~(df["shift"]=="qmc")]
rprqmc_df=df[(df["DrawMethod"].isin(RpRQMC))&~(df["shift"]=="qmc")]
qmc_df=df[df["shift"]=="qmc"]
dfs=[fprqmc_df,rprqmc_df,qmc_df]
for d in dfs:
    d=d[d["rDrawn"]==11]
    d=d[d["MedianOfMeans"]>0]

#smap=lambda x:np.sqrt(x)*12
smap=lambda x:x*3
r=11
dff=fprqmc_df[fprqmc_df["rDrawn"]==r]
dfr=rprqmc_df[rprqmc_df["rDrawn"]==r]
dfq=qmc_df[qmc_df["rDrawn"]==r]
ax[0].scatter(np.abs(dff["skew"]),
    dff["kurt"],
    s=smap(dff["dotsize"]),
    c=dff["dotcolor"],
    edgecolors="black",
    linewidths=0.2)
ax[1].scatter(np.abs(dfr["skew"]),
    dfr["kurt"],
    s=smap(dfr["dotsize"]),
    c=dfr["dotcolor"],
    edgecolors="black",
    linewidths=0.2)
ax[2].scatter(np.abs(dfq["skew"]),
    dfq["kurt"],
    s=smap(dfq["dotsize"]),
    c=dfq["dotcolor"],
    edgecolors="black",
    linewidths=0.3)
for i in range(len(ax)):
    ax[i].plot(cauchschwartz_skew,
        cauchyschwartz_kurt,
        color="gray")

yoffset=1.03
fontsize=11
ax[0].set_title("Category (a)",y=yoffset,fontsize=fontsize)
ax[1].set_title("Category (b)",y=yoffset,fontsize=fontsize)
ax[2].set_title("Category (c)",y=yoffset,fontsize=fontsize)
ax[0].set_ylabel(r"$\kappa$")
ax[0].set_xlabel(r"$|\gamma|$")
ax[1].set_xlabel(r"$|\gamma|$")
ax[2].set_xlabel(r"$|\gamma|$")
ax[0].set_xscale("log",base=10)
ax[0].set_yscale("log",base=10)
ax[0].set_xlim(8e-5/5, 1.2e3/5)
ax[0].set_xticks(10**(np.arange(-4,4,2).astype(float)))
ax[0].set_ylim(0.9,1.1e4)

outname=os.path.join(os.path.dirname(infile),"Fig3_r11.pdf")
fig.savefig(outname,bbox_inches="tight")
# %%
extreme_dicts=[
    dff[dff["ratio"]==np.max(dff["ratio"])],
    dff[dff["ratio"]==np.min(dff["ratio"])],
    dff[dff["dotsize"]==np.min(dff["dotsize"])],
    dfr[dfr["ratio"]==np.max(dfr["ratio"])],
    dfr[dfr["ratio"]==np.min(dfr["ratio"])],
    dfr[dfr["dotsize"]==np.min(dfr["dotsize"])],
    dfq[dfq["ratio"]==np.max(dfq["ratio"])],
    dfq[dfq["ratio"]==np.min(dfq["ratio"])],
    dfq[dfq["dotsize"]==np.min(dfq["dotsize"])],
]


#%%
extreme_df=pd.concat(extreme_dicts,ignore_index=True)
cols=['TestFunction', 'DrawMethod', 'dim', 'nPoints', 'log2n', 'shift',
       'baker', 'rDrawn', 'mean', 'var', 'skew', 'kurt', 'MeanOfMeans',
       'MedianOfMeans', 'LeeValiant', 'MinskerNdaoud(3)', 'MinskerNdaoud(2)',
       'MinskerNdaoud(3;1.0)', 'ratio', 'dotsize', 'dotcolor']
dropcols=["LeeValiant"]
if "rhofile" in extreme_df.columns:
    dropcols.append("rhofile")
dropcols.extend(cols[-7:])
#%%
extreme_df=extreme_df.drop(columns=dropcols)
extreme_df=extreme_df.rename(columns={
    "MeanOfMeans":"MSE[A_r]",
    "MedianOfMeans":"MSE[M_r]"
})
extreme_df["ratio"]=extreme_df["MSE[A_r]"]/extreme_df["MSE[M_r]"]



extreme_df.to_csv(os.path.join(os.path.dirname(infile),
    "fig3_r11_extremevals.csv"),index=False)
df=df.drop(columns=dropcols)
df=df.rename(columns={
    "MeanOfMeans":"MSE[A_r]",
    "MedianOfMeans":"MSE[M_r]"
})
df.to_csv(os.path.join(os.path.dirname(infile),
    "SAMOmse.csv"),index=False)
# %%
