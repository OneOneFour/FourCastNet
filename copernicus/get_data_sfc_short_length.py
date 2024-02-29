import cdsapi

c = cdsapi.Client()

c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type': 'reanalysis',
        'format': 'netcdf',
        'variable': [
            '10m_u_component_of_wind', '10m_v_component_of_wind', '2m_temperature',
            'mean_sea_level_pressure', 'surface_pressure', 'total_column_water_vapour',
        ],
        'year': '2024',
        'month': '2',
        'day': [
            '15','16','17'
        ],
        'time': [
            '00:00', '06:00', '12:00',
            '18:00',
        ],
    },
    '/scratch/users/robcking/2024_era5_FCN_surface.nc')


#    '/project/projectdirs/dasrepo/ERA5/oct_2021_19_31_pl.nc')
