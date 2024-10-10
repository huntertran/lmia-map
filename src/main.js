import 'ol/ol.css';
import Feature from 'ol/Feature';
import Point from 'ol/geom/Point';
import VectorSource from 'ol/source/Vector';
import Cluster from 'ol/source/Cluster';
import VectorLayer from 'ol/layer/Vector';
import Style from 'ol/style/Style';
import CircleStyle from 'ol/style/Circle';
import Stroke from 'ol/style/Stroke';
import Fill from 'ol/style/Fill';
import Text from 'ol/style/Text';
import Overlay from 'ol/Overlay';
import OLMap from 'ol/Map';
import View from 'ol/View';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import { useGeographic } from 'ol/proj';
import Papa from 'papaparse';

// Set coordinate system to [longitude, latitude]
useGeographic();

// Constants
const UPDATED_DATE = '20241009';
const DEFAULT_STROKE_COLOR = '#fff';
const DEFAULT_FILL_COLOR = '#FF0000';
const TEXT_FILL_COLOR = '#fff';
const MAP_CENTER = [-79.3832, 43.6532]; // Toronto
const INITIAL_ZOOM = 7;
const styleCache = {};
const allEmployers = new Map();

const element = document.getElementById('popup');
const popup = new Overlay({
  element: element,
  positioning: 'bottom-center',
  stopEvent: false,
});

let vectorSource = new VectorSource();
let clusterSource = new Cluster({
  distance: 40,
  source: vectorSource
});
let popover;

// Helper Functions
function createStroke(color = DEFAULT_STROKE_COLOR) {
  return new Stroke({ color });
}

function createFill(color = DEFAULT_FILL_COLOR) {
  return new Fill({ color });
}

function createText(size) {
  return new Text({
    text: size.toString(),
    fill: createFill(TEXT_FILL_COLOR)
  });
}

function createStyle(size) {
  return new Style({
    image: new CircleStyle({
      radius: 10,
      stroke: createStroke(),
      fill: createFill()
    }),
    text: createText(size)
  });
}

function getStyle(size) {
  if (!styleCache[size]) {
    styleCache[size] = createStyle(size);
  }
  return styleCache[size];
}

function buyCoffee() {
  window.open('https://buymeacoffee.com/huntertran', '_blank');
}

function showInfo() {
  window.open('https://open.canada.ca/data/en/dataset/90fed587-1364-4f33-a9ee-208181dc0b97', '_blank');
}

function initMap() {
  var clusters = new VectorLayer({
    source: clusterSource,
    style: function (feature, resolution) {
      var size = feature.get('features').length;
      return getStyle(size);
    }
  });

  var map = new OLMap({
    target: document.getElementById('map'),
    layers: [
      new TileLayer({
        source: new OSM(),
      }),
      clusters
    ],
    view: new View({
      center: MAP_CENTER,
      zoom: INITIAL_ZOOM,
    }),
  });

  registerPopup(map);
  registerPointer(map);
}

function disposePopover() {
  if (popover) {
    popover.dispose();
    popover = undefined;
  }
}

function getClusterContent(features) {
  let content = '';
  if (features.length <= 10) {
    content = '<div class="popover-content"><ul>';
    features.forEach(feature => {
      const employerId = feature.get('emId');
      const employer = allEmployers.get(employerId);
      if (employer) {
        content += `<li><strong>${employer.Employer}</strong><br>${employer.Address}</li>`;
      }
    });
    content += '</ul></div>';
  }
  else {
    let sumPos = 0;
    features.forEach(feature => {
      const pos = feature.get('pos');
      sumPos += pos;
    });
    content = `Total <strong>${features.length}</strong> employers`;
    content += "<br>";
    content += `Number of LMIA positions: <strong>${sumPos}</strong>`;
  }
  return content;
}

function onClusterClicked(map, evt) {
  const feature = map.forEachFeatureAtPixel(evt.pixel, function (feature) {
    return feature;
  });

  disposePopover(popover);

  if (!feature) {
    return;
  }

  popup.setPosition(evt.coordinate);

  popover = new bootstrap.Popover(element, {
    placement: 'auto',
    html: true,
    content: getClusterContent(feature.get('features')),
    boundary: 'window'
  });

  popover.show();
}

function registerPopup(map) {
  map.addOverlay(popup);

  // display popup on click
  map.on('click', function (evt) {
    return onClusterClicked(map, evt);
  });
}

function registerPointer(map) {
  // change mouse cursor when over marker
  map.on('pointermove', function (e) {
    const pixel = map.getEventPixel(e.originalEvent);
    const hit = map.hasFeatureAtPixel(pixel);
    map.getTarget().style.cursor = hit ? 'pointer' : '';
  });
  // Close the popup when the map is moved
  map.on('movestart', disposePopover);
}

function loadData(file) {
  var features = [];

  fetch(file)
    .then(response => response.text())
    .then(csvText => {
      Papa.parse(csvText, {
        header: true,
        dynamicTyping: true,
        complete: function (results) {
          results.data.forEach(row => {
            var coordinates = [row.Longitude, row.Latitude];
            var feature = new Feature(new Point(coordinates));
            feature.setProperties({
              'emId': row.EmployerID,
              'pos': row.Position
            });
            features.push(feature);
          });

          vectorSource.clear();
          vectorSource.addFeatures(features);
          clusterSource.setSource(vectorSource);
        }
      });
    })
    .catch(error => console.error('Error fetching the CSV file:', error));
}

function loadEmployers() {
  Papa.parse('data/all_employers.csv?updated=' + UPDATED_DATE, {
    header: true,
    dynamicTyping: true,
    download: true,
    complete: function (results) {
      results.data.forEach(row => {
        allEmployers.set(row.ID, row);
      });
    },
    error: function (error) {
      console.error('Error fetching all_employers.csv: ', error);
    }
  });
}

function onSliderInput(year) {
  document.getElementById('yearLabel').innerText = year;
  loadData('data/' + year + '.csv');
}

// Ensure the function is available globally
window.onSliderInput = onSliderInput;
window.buyCoffee = buyCoffee;
window.showInfo = showInfo;

initMap();
// Fetch the CSV file
loadData('data/2024.csv');
loadEmployers();