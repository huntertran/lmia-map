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
import Map from 'ol/Map';
import View from 'ol/View';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import { useGeographic } from 'ol/proj';
import Papa from 'papaparse';

// Set coordinate system to [longitude, latitude]
useGeographic();

// Constants
const DEFAULT_STROKE_COLOR = '#fff';
const DEFAULT_FILL_COLOR = '#FF0000';
const TEXT_FILL_COLOR = '#fff';
const MAP_CENTER = [-79.3832, 43.6532];
const INITIAL_ZOOM = 7;
const styleCache = {};

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

// Main Code
var features = [];

fetch('data/2014.csv')
  .then(response => response.text())
  .then(csvText => {
    Papa.parse(csvText, {
      header: true,
      dynamicTyping: true,
      complete: function (results) {
        results.data.forEach(row => {
          var coordinates = [row.Longitude, row.Latitude];
          features.push(new Feature(new Point(coordinates)));
        });

        var source = new VectorSource({
          features: features
        });

        var clusterSource = new Cluster({
          distance: 40,
          source: source
        });

        var clusters = new VectorLayer({
          source: clusterSource,
          style: function (feature, resolution) {
            var size = feature.get('features').length;
            return getStyle(size);
          }
        });

        var map = new Map({
          target: 'map',
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
      }
    });
  })
  .catch(error => console.error('Error fetching the CSV file:', error));