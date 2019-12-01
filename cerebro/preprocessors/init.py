import cerebro.preprocessors.Image_population as Image_pop

a = Image_pop.Image_population('tmp', (400, 400))
b = a.filter('Gabor')
c = a.intensity_to_latensy(b)
print(c)
