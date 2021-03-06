var chartifySetPricing = function(selector, setCode, collectorNumber) {
    // set the dimensions and margins of the graph
    var margin = {top: 10, right: 30, bottom: 30, left: 60},
        width = 460 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = d3.select(selector)
      .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");

    d3.json(`/pricing/chart/${setCode}/${collectorNumber}`,
      function(data) {
        // Add X axis --> it is a date format
        var x = d3.scaleTime()
          .domain(d3.extent(data, function(d) {
              return new Date(d.date);
          }))
          .range([ 0, width ]);
        svg.append("g")
          .attr("transform", "translate(0," + height + ")")
          .call(d3.axisBottom(x));

        // Add Y axis
        var y = d3.scaleLinear()
          .domain([0, d3.max(data, function(d) { return +d.pricing.highPrice || d.pricing.high_price; })])
          .range([ height, 0 ]);
        svg.append("g")
          .call(d3.axisLeft(y));

        // Add the line
        svg.append("path")
          .datum(data)
          .attr("fill", "none")
          .attr("stroke", "steelblue")
          .attr("stroke-width", 1.5)
          .attr("d", d3.line()
            .x(function(d) {
                return x(new Date(d.date));
            })
            .y(function(d) {
                return y(d.pricing.marketPrice || d.pricing.market_price);
            })
            );

        svg.append("path")
          .datum(data)
          .attr("fill", "none")
          .attr("stroke", "green")
          .attr("stroke-width", 1)
          .attr("d", d3.line()
            .x(function(d) {
                return x(new Date(d.date));
            })
            .y(function(d) {
                return y(d.pricing.lowPrice || d.pricing.low_price);
            })
            );

        svg.append("path")
          .datum(data)
          .attr("fill", "none")
          .attr("stroke", "red")
          .attr("stroke-width", 1)
          .attr("d", d3.line()
            .x(function(d) {
                return x(new Date(d.date));
            })
            .y(function(d) {
                return y(d.pricing.highPrice || d.pricing.high_price);
            })
            );

    });
};

window.onload = function () {
    chartifySetPricing('#pricing-chart', SET_CODE, COLLECTOR_NUMBER);
};
