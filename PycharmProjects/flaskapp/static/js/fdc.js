//
//$(function(){
//    $('#btn-Visualization').click(function(){
//        $.getJSON({
//        url:"/visualize",
//        data:link,fdc_link,
//        success: function
//
//        })
//    });
//});

function show(){

    var links = [
      {source: "吃", target: "他", type: "suit"},
      {source: "吃", target: "把", type: "suit"},
      {source: "把", target: "苹果", type: "suit"},
      {source: "吃", target: "了", type: "suit"},
      {source: "吃", target: "。", type: "suit"}
    ];

    var nodes = {};

    links.forEach(function(link) {
      link.source = nodes[link.source] || (nodes[link.source] = {name: link.source});
      link.target = nodes[link.target] || (nodes[link.target] = {name: link.target});
    });

    var w = 960,
        h = 500;

    var force = d3.layout.force()
        .nodes(d3.values(nodes))
        .links(links)
        .size([w, h])
        .linkDistance(60)
        .charge(-300)
        .on("tick", tick)
        .start();

    var svg = d3.select("dcg").append("svg:svg")
        .attr("width", w)
        .attr("height", h);

    //(1)创建箭头
    svg.append("svg:defs").selectAll("marker")
        .data(["suit", "licensing", "resolved"])
      .enter().append("svg:marker")
        .attr("id", String)
        .attr("viewBox", "0 -5 10 10")
        .attr("refX", 15)
        .attr("refY", -1.5)
        .attr("markerWidth", 6)
        .attr("markerHeight", 6)
        .attr("orient", "auto")
      .append("svg:path")
        .attr("d", "M0,-5L10,0L0,5");
    //(2)根据连线类型引用上面创建的标记
    var path = svg.append("svg:g").selectAll("path")
        .data(force.links())
      .enter().append("svg:path")
        .attr("class", function(d) { return "link " + d.type; })
        .attr("marker-end", function(d) { return "url(#" + d.type + ")"; });

    var circle = svg.append("svg:g").selectAll("circle")
        .data(force.nodes())
      .enter().append("svg:circle")
        .attr("r", 6)
        .call(force.drag);

    var text = svg.append("svg:g").selectAll("g")
        .data(force.nodes())
      .enter().append("svg:g");

    // A copy of the text with a thick white stroke for legibility.
    text.append("svg:text")
        .attr("x", 8)
        .attr("y", ".31em")
        .attr("class", "shadow")
        .text(function(d) { return d.name; });

    text.append("svg:text")
        .attr("x", 8)
        .attr("y", ".31em")
        .text(function(d) { return d.name; });

    // 使用椭圆弧路径段双向编码。
    function tick() {
    //(3)打点path格式是：Msource.x,source.yArr00,1target.x,target.y
      path.attr("d", function(d) {
        var dx = d.target.x - d.source.x,//增量
            dy = d.target.y - d.source.y,
            dr = Math.sqrt(dx * dx + dy * dy);
        return "M" + d.source.x + ","
        + d.source.y + "A" + dr + ","
        + dr + " 0 0,1 " + d.target.x + ","
        + d.target.y;
      });

      circle.attr("transform", function(d) {
        return "translate(" + d.x + "," + d.y + ")";
      });

      text.attr("transform", function(d) {
        return "translate(" + d.x + "," + d.y + ")";
      });
    }
}
