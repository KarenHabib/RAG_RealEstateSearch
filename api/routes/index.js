const express = require('express');
const router = express.Router();
const path = require('path');
const csv = require('csv-parser');
const fs = require('fs');

router.get('/properties', (req, res) => {
  const results = [];
  fs.createReadStream(path.resolve(__dirname, '../../data/uae_real_estate_2024.csv'))
    .pipe(csv())
    .on('data', (data) => {
      results.push(data);
    })
    .on('end', () => {
      const filteredProperties = results.filter(property => {
        return (
          (!req.query.bedrooms || property.bedrooms == req.query.bedrooms) &&
          (!req.query.bathrooms || property.bathrooms == req.query.bathrooms) &&
          (!req.query.location || property.displayAddress.includes(req.query.location)) &&
          (!req.query.price || property.price <= req.query.price)
        );
      });
      res.json(filteredProperties);
    });
});

module.exports = router;