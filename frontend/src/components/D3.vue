<template>
    <div>
        <div ref="d3container"></div>
    </div>
</template>
  
  <script>
  import * as d3 from "d3";
  
  export default {
    props: {
      name: String,
      data: Array,
    },
    data() {
      return {
        svg: null,
      };
    },
    mounted() {
        this.drawChart();
    },
    methods: {
      drawChart() {
        // la lista di array in un unico array
        const flattenedData = this.data.flat();
  
        const color = d3.scaleOrdinal(d3.schemeCategory10);

        // Raggruppare e sommare i dati per etichetta
        const aggregatedData = Array.from(
          d3.group(flattenedData, d => d.label),
          ([label, values]) => ({label, score: d3.sum(values, d => d.score)})
        );
  
        const container = d3.select(this.$refs.d3container);
        const width = 350;
        const height = 400;
  
        this.svg = container.append("svg")
          .attr("width", width)
          .attr("height", height);
  
        const pack = d3.pack()
          .size([width, height])
          .padding(1.5);
  
        const root = d3.hierarchy({children: aggregatedData})
          .sum(d => d.score);
  
        const bubbles = pack(root).leaves();
  
        this.svg.selectAll("circle")
          .data(bubbles)
          .enter()
          .append("circle")
          .attr("cx", d => d.x)
          .attr("cy", d => d.y)
          .attr("r", d => d.r)
          .style("fill", d => color(d.data.label)); 
  
        // Aggiungi etichette ai cerchi
        this.svg.selectAll("text")
          .data(bubbles)
          .enter()
          .append("text")
          .attr("x", d => d.x)
          .attr("y", d => d.y)
          .text(d => d.data.label)
          .attr("text-anchor", "middle")
          .style("fill", "black");
      }
    }
  };
  </script>
  