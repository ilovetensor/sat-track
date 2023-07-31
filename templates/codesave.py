"""``
    
// getting data from satellite-js

const ISS_TLE = 
`1 43698U 18089A   23205.32132730  .00000097  00000+0  00000+0 0  9993
2 43698   0.0301 272.1108 0002422 169.3789  31.0375  1.00273980 17175`


const satrec = satellite.twoline2satrec(
    ISS_TLE.split('\n')[0].trim(), 
    ISS_TLE.split('\n')[1].trim()
  );


    const totalSeconds = 60 * 60 * 24;
    const timestepInSeconds = 10;
    const start = Cesium.JulianDate.fromDate(new Date());
    const stop = Cesium.JulianDate.addSeconds(start, totalSeconds, new Cesium.JulianDate());
    viewer.clock.startTime = start.clone();
    viewer.clock.stopTime = stop.clone();
    viewer.clock.currentTime = start.clone();
    viewer.timeline.zoomTo(start, stop);
    //viewer.clock.multiplier = 40;
    viewer.clock.clockRange = Cesium.ClockRange.LOOP_STOP;
    
    const positionsOverTime = new Cesium.SampledPositionProperty();
    for (let i = 0; i < totalSeconds; i+= timestepInSeconds) {
      const time = Cesium.JulianDate.addSeconds(start, i, new Cesium.JulianDate());
      const jsDate = Cesium.JulianDate.toDate(time);

      const positionAndVelocity = satellite.propagate(satrec, jsDate);
      const gmst = satellite.gstime(jsDate);
      const p   = satellite.eciToGeodetic(positionAndVelocity.position, gmst);
      
      const position = Cesium.Cartesian3.fromRadians(p.longitude, p.latitude, p.height * 1000);

      //console.log(time)
      positionsOverTime.addSample(time, position);
     
    } 

// getting live data from both satellitejs and skyfield
function get_live_data() {

    const div_data = document.getElementById('data');
    //const div_satellitejs = document.getElementById('data-satellitejs');

    const time_now = Cesium.JulianDate.fromDate(new Date());
    //const jsDate_now = Cesium.JulianDate.toDate(time_now);

    //const positionAndVelocity = satellite.propagate(satrec, jsDate_now);
    //const gmst = satellite.gstime(jsDate_now);
    
    //const p   = satellite.eciToGeodetic(positionAndVelocity.position, gmst);
    
    //div_satellitejs.innerHTML = `latitude : ${r2d(p.latitude, 2)}, longitude: ${r2d(p.longitude,2 )}, height: ${Math.round(p.height *100)/100}, UTC: ${time_now.toString().slice(11, 19)}`;
    

    $.ajax({ 
      url: "{% url 'data' %}",
      type: "GET",
      dataType: "json",
      success: (data) => {

        div_data.innerHTML = `latitude : ${data.context.lat}, longitude: ${data.context.lon}, height: ${data.context.height}, UTC: ${data.context.time}`;
        //console.log(data.context);
      },
      error: (error) => {
        console.log(error);
      }
    });


"""