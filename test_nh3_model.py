import numpy as np
from pyspeckit.spectrum.models import ammonia
import pytest
import pyspeckit

"""
Test nh3 model against Erik's IDL-based code


function nh3model, v, nu = nu, n11 = n11, n22 = n22, n33 = n33, n44 = n44, $
             str = s, tkin = tkin, logn = logn, v0 = v0, sigv = sigv, $
             tautex = tautex, fortho = fortho, tex = tex

v = findgen(150)*0.4 - 30
print,v
ckms = 2.99792458d5
print,(1-v/ckms)*23.6944955d9
testspec = nh3model(v, /n11, tkin=20., tex=20., logn=14., sigv=1.0, fortho=0.5, v0=0.)
print,testspec

v = findgen(150)*0.4 - 30
print,v
ckms = 2.99792458d5
print,(1-v/ckms)*23.6944955d9
testspec2 = nh3model(v, /n11, tkin=30., tex=10., logn=14., sigv=1.0, fortho=0.5, v0=0.)
print,testspec2

Test against Charles Figura's NH3
v = findgen(150)*0.4 - 30
sigv = 1.0*sqrt(8*alog(2.D))
amp = 1.0 ; amplitude of main?
tau = 0.5
vcen = 0.0
a = [amp, tau, vcen, sigv]
ammonias11hfs_new, v, a, f, pder
print,f
"""

xarr_idl_str = """
   2.3696867e+10   2.3696835e+10   2.3696803e+10   2.3696772e+10   2.3696740e+10   2.3696709e+10   2.3696677e+10   2.3696645e+10   2.3696614e+10
   2.3696582e+10   2.3696550e+10   2.3696519e+10   2.3696487e+10   2.3696456e+10   2.3696424e+10   2.3696392e+10   2.3696361e+10   2.3696329e+10
   2.3696298e+10   2.3696266e+10   2.3696234e+10   2.3696203e+10   2.3696171e+10   2.3696139e+10   2.3696108e+10   2.3696076e+10   2.3696045e+10
   2.3696013e+10   2.3695981e+10   2.3695950e+10   2.3695918e+10   2.3695887e+10   2.3695855e+10   2.3695823e+10   2.3695792e+10   2.3695760e+10
   2.3695728e+10   2.3695697e+10   2.3695665e+10   2.3695634e+10   2.3695602e+10   2.3695570e+10   2.3695539e+10   2.3695507e+10   2.3695476e+10
   2.3695444e+10   2.3695412e+10   2.3695381e+10   2.3695349e+10   2.3695317e+10   2.3695286e+10   2.3695254e+10   2.3695223e+10   2.3695191e+10
   2.3695159e+10   2.3695128e+10   2.3695096e+10   2.3695065e+10   2.3695033e+10   2.3695001e+10   2.3694970e+10   2.3694938e+10   2.3694906e+10
   2.3694875e+10   2.3694843e+10   2.3694812e+10   2.3694780e+10   2.3694748e+10   2.3694717e+10   2.3694685e+10   2.3694654e+10   2.3694622e+10
   2.3694590e+10   2.3694559e+10   2.3694527e+10   2.3694496e+10   2.3694464e+10   2.3694432e+10   2.3694401e+10   2.3694369e+10   2.3694337e+10
   2.3694306e+10   2.3694274e+10   2.3694243e+10   2.3694211e+10   2.3694179e+10   2.3694148e+10   2.3694116e+10   2.3694085e+10   2.3694053e+10
   2.3694021e+10   2.3693990e+10   2.3693958e+10   2.3693926e+10   2.3693895e+10   2.3693863e+10   2.3693832e+10   2.3693800e+10   2.3693768e+10
   2.3693737e+10   2.3693705e+10   2.3693674e+10   2.3693642e+10   2.3693610e+10   2.3693579e+10   2.3693547e+10   2.3693515e+10   2.3693484e+10
   2.3693452e+10   2.3693421e+10   2.3693389e+10   2.3693357e+10   2.3693326e+10   2.3693294e+10   2.3693263e+10   2.3693231e+10   2.3693199e+10
   2.3693168e+10   2.3693136e+10   2.3693104e+10   2.3693073e+10   2.3693041e+10   2.3693010e+10   2.3692978e+10   2.3692946e+10   2.3692915e+10
   2.3692883e+10   2.3692852e+10   2.3692820e+10   2.3692788e+10   2.3692757e+10   2.3692725e+10   2.3692693e+10   2.3692662e+10   2.3692630e+10
   2.3692599e+10   2.3692567e+10   2.3692535e+10   2.3692504e+10   2.3692472e+10   2.3692441e+10   2.3692409e+10   2.3692377e+10   2.3692346e+10
   2.3692314e+10   2.3692282e+10   2.3692251e+10   2.3692219e+10   2.3692188e+10   2.3692156e+10
"""

testspec_idl_str = """
       0.0000000       0.0000000       0.0000000       0.0000000       0.0000000       0.0000000       0.0000000   1.9135795e-14   3.7697515e-13
   6.3703061e-12   9.1861383e-11   1.1294750e-09   1.1839492e-08   1.0580753e-07   8.0616631e-07   5.2368360e-06   2.9003903e-05   0.00013695986
   0.00055142509    0.0018929080    0.0055400651     0.013823619     0.029404787     0.053321606     0.082436362      0.10868616      0.12223634
      0.11729411     0.096023908     0.067051113     0.039924511     0.020268059    0.0087725097    0.0032374212    0.0010187798   0.00027339542
   6.2566847e-05   1.2210934e-05   2.0323888e-06   2.8851603e-07   3.5387596e-08   8.7448587e-09   4.8568869e-08   3.8652753e-07   2.6425374e-06
   1.5426704e-05   7.6931356e-05   0.00032790160    0.0011952383    0.0037285769    0.0099619887     0.022815614     0.044834537     0.075675520
      0.10985076      0.13732061      0.14800828      0.13766796      0.11054538     0.076625464     0.045831096     0.023640645     0.010510204
    0.0040306060    0.0013709608   0.00061114372    0.0011254490    0.0038909377     0.012393061     0.033892588     0.079260447      0.15847517
      0.27100397      0.39674268      0.49797092      0.53667150      0.49701727      0.39545745      0.27008609      0.15819155     0.079424753
     0.034186370     0.012620468    0.0040079424    0.0011512351   0.00054236625    0.0011331575    0.0034686900    0.0094567385     0.022102147
     0.044205897     0.075689391      0.11101017      0.13957184      0.15054336      0.13937328      0.11077209     0.075575987     0.044255776
     0.022240469    0.0095914939    0.0035494245    0.0011269316   0.00030688722   7.1655378e-05   1.4339347e-05   2.4581414e-06   3.6086692e-07
   4.5956093e-08   1.1613818e-08   6.1999681e-08   4.7935010e-07   3.1847898e-06   1.8062023e-05   8.7463161e-05   0.00036177110    0.0012788397
    0.0038654639    0.0099969283     0.022136193     0.041999946     0.068346207     0.095493423      0.11469525      0.11855183      0.10554158
     0.080964799     0.053530494     0.030501510     0.014975614    0.0063337271    0.0023063569   0.00072261042   0.00019463863   4.5031177e-05
   8.9404465e-06   1.5217973e-06   2.2189477e-07   2.7693144e-08   2.9562048e-09   2.6975940e-10   2.1030253e-11   1.4007412e-12   8.0370394e-14
   3.8271617e-15       0.0000000       0.0000000       0.0000000       0.0000000       0.0000000
"""

testspec_idl_str2 = """
       0.0000000       0.0000000       0.0000000       0.0000000       0.0000000       0.0000000   8.0395504e-16   1.2863281e-14   2.5806957e-13
   4.3711037e-12   6.3042137e-11   7.7512847e-10   8.1251336e-09   7.2612931e-08   5.5325076e-07   3.5939027e-06   1.9904607e-05   9.3991721e-05
   0.00037842474    0.0012990079    0.0038016142    0.0094843767     0.020168827     0.036557350     0.056488160     0.074439374     0.083698995
     0.080322225     0.065782329     0.045958696     0.027379038     0.013904256    0.0060193730    0.0022216252   0.00069914883   0.00018762318
   4.2937940e-05   8.3800422e-06   1.3947752e-06   1.9800100e-07   2.4285581e-08   6.0013674e-09   3.3331544e-08   2.6526374e-07   1.8135042e-06
   1.0586940e-05   5.2795904e-05   0.00022502894   0.00082024281    0.0025586496    0.0068354009     0.015651194     0.030743413     0.051861872
     0.075235407     0.094001508      0.10129766     0.094238678     0.075710173     0.052511969     0.031426187     0.016216909    0.0072114857
    0.0027658949   0.00094083093   0.00041940729   0.00077235033    0.0026700582    0.0085030973     0.023245109     0.054315108      0.10844030
      0.18505497      0.27028346      0.33860604      0.36465745      0.33796361      0.26941435      0.18443134      0.10824680     0.054427541
     0.023446474    0.0086590903    0.0027503440   0.00079004598   0.00037220815   0.00077764033    0.0023803200    0.0064887859     0.015161968
     0.030312706     0.051871375     0.076027863     0.095538610      0.10302788     0.095403044     0.075865144     0.051793767     0.030346882
     0.015256818    0.0065812331    0.0024357191   0.00077336793   0.00021060755   4.9175163e-05   9.8407196e-06   1.6869586e-06   2.4765361e-07
   3.1538475e-08   7.9702630e-09   4.2548774e-08   3.2896556e-07   2.1856386e-06   1.2395494e-05   6.0023606e-05   0.00024827249   0.00087761395
    0.0026525794    0.0068593727     0.015185315     0.028801223     0.046845295     0.065419586     0.078546349     0.081181662     0.072289876
     0.055481330     0.036700443     0.020920663     0.010274548    0.0043461673    0.0015827261   0.00049590228   0.00013357499   3.0903708e-05
   6.1355966e-06   1.0443702e-06   1.5228065e-07   1.9005089e-08   2.0287673e-09   1.8512940e-10   1.4432621e-11   9.6072765e-13   5.4669022e-14
   2.4118686e-15       0.0000000       0.0000000       0.0000000       0.0000000       0.0000000
"""

# abandoned this comparison because this approach uses an arbitrary T_astar
# scaling and is therefore not readily compared
testspec_figura_str = """
       0.0000000       0.0000000       0.0000000       0.0000000       0.0000000   2.2318416e-17   8.0064868e-16   1.7397448e-14   3.2135075e-13
   5.0803086e-12   6.8701383e-11   7.9476600e-10   7.8659774e-09   6.6610570e-08   4.8266371e-07   2.9929144e-06   1.5882667e-05   7.2136546e-05
   0.00028040855   0.00093279278    0.0026547375    0.0064610874     0.013441206     0.023900043     0.036352310     0.047378274     0.053014002
     0.050986712     0.042131286     0.029861422     0.018119131    0.0094003081    0.0041686854    0.0015807206   0.00051278216   0.00014236386
   3.3832906e-05   6.8830021e-06   1.1986980e-06   1.7872220e-07   2.3138261e-08   5.9869568e-09   3.1296970e-08   2.3636047e-07   1.5405535e-06
   8.6070131e-06   4.1236195e-05   0.00016950520   0.00059812948    0.0018126912    0.0047198446     0.010561898     0.020323544     0.033669083
     0.048129845     0.059547082     0.063944429     0.059689378     0.048415919     0.034064981     0.020746122     0.010919080    0.0049629489
    0.0019510547   0.00068475505   0.00031988795   0.00058679485    0.0019586387    0.0060424012     0.016028682     0.036330346     0.070245007
      0.11597792      0.16431094      0.20135531      0.21508893      0.20094358      0.16371038      0.11547770     0.070004371     0.036315080
     0.016111746    0.0061251078    0.0020056334   0.00059647327   0.00028606571   0.00057293120    0.0016947487    0.0044961390     0.010256594
     0.020067515     0.033691358     0.048619538     0.060464164     0.064964150     0.060377156     0.048509774     0.033629301     0.020075421
     0.010307479    0.0045508009    0.0017282685   0.00056478953   0.00015884366   3.8441685e-05   8.0028681e-06   1.4325369e-06   2.2041820e-07
   2.9568873e-08   7.8127883e-09   3.9303689e-08   2.8861581e-07   1.8299054e-06   9.9418496e-06   4.6297854e-05   0.00018488031   0.00063334133
    0.0018618700    0.0046982713     0.010179083     0.018944850     0.030326101     0.041840398     0.049885059     0.051513681     0.046120629
     0.035784453     0.024029231     0.013945847    0.0069897304    0.0030246186    0.0011298936   0.00036431013   0.00010133559   2.4299920e-05
   5.0192909e-06   8.9225575e-07   1.3638800e-07   1.7912160e-08   2.0196733e-09   1.9538550e-10   1.6207512e-11   1.1521974e-12   7.0151849e-14
   3.6541195e-15   1.5732478e-16   1.0976864e-18       0.0000000       0.0000000       0.0000000
"""

@pytest.mark.parametrize(('testspec_idl_str','tex','tkin'),
                         ((testspec_idl_str, testspec_idl_str2),
                          (20, 10),
                          (20, 30))
                        )
def test_eriks_idl(testspec_idl_str, tex, tkin, plot=False):
    idl_test_xarr = np.array(xarr_idl_str.split(), dtype='float')
    idl_test_spectrum = np.array(testspec_idl_str.split(), dtype='float')

    refX = 23.6944955e9 # from nh3model.pro
    refX = 23.694506e9 # from modelspec.pro

    xarr11 = pyspeckit.units.SpectroscopicAxis(np.arange(-30,30,0.4),
                                               unit='km/s', refX=refX,
                                               refX_unit='Hz', frame='LSRK',
                                               xtype='Frequency')

    # The two arrays are shifted in frequency because nh3model.pro converts to
    # frequency with a different reference; the reference frequency is not centered
    # on any of the individual lines
    #print np.array(xarr11.as_unit('Hz')) - idl_test_xarr

    ps_spectrum = ammonia.ammonia(xarr11, tkin=tkin, tex=tex, ntot=14, width=1,
                                  xoff_v=0.0, fortho=0.5, )

    absfracdiff = np.abs((idl_test_spectrum - ps_spectrum)/idl_test_spectrum * (np.abs(idl_test_spectrum) > 0))

    if plot:
        import pylab as pl
        fig1 = pl.figure(1)
        fig1.clf()
        ax1 = fig1.gca()
        ax1.plot(idl_test_xarr, idl_test_spectrum, label="IDL")
        ax1.plot(xarr11.as_unit('Hz'), ps_spectrum, label="pyspeckit")
        ax1.set_xlabel("Frequency (Hz)")
        ax1.set_ylabel("Test spectra")
        pl.legend(loc='best')

        fig2 = pl.figure(2)
        fig2.clf()
        ax2 = fig2.gca()
        ax2.plot(xarr11, np.abs(idl_test_spectrum - ps_spectrum)/idl_test_spectrum)
        ax2.set_xlabel("Frequency (Hz)")
        ax2.set_ylabel("(IDL-pyspeckit)/IDL")

        pl.draw()
        pl.show()

    assert np.nanmax(absfracdiff) < 0.01

    return absfracdiff
