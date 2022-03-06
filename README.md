## I have moved this work over to [here](https://github.com/colour-science/colour/pull/824).

# Helmholtz-Kohlrausch effect
Here I have implemented "Simple Estimation Methods for the Helmholtz – Kohlrausch Effect" by Nayatani.

Running the code generates the following images:

### Helmholtz-Kohlrausch effect in action:
![HKE demo](/images/equal_Y.png)
All of the patches in this image have the same Y (luminance) value as the background, however they look very different in terms of brightness thanks to the Helmholtz-Kohlrausch effect.

This shows that luminance is not equal to brightness.

### Same image, but HKE compensated for:
![HKE demo](/images/HKE_compensated.png)
Here I have tried to compensate for the HKE effect using the VCC for luminous colours model from Nayatani. I would say it has overcompensated, as the red, purple and blue look slightly too dark to me.
