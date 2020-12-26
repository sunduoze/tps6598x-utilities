/* Copyright 2015 Bloomberg Finance L.P.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

define(["./components/d3/d3", "./Mark"], function(d3, MarkViewModule) {
    "use strict";

    var OHLC = MarkViewModule.Mark.extend({
        render: function() {
            var base_creation_promise = OHLC.__super__.render.apply(this);

            var that = this;
            this.displayed.then(function() {
                that.parent.tooltip_div.node().appendChild(that.tooltip_div.node());
                that.create_tooltip();
            });

            return base_creation_promise.then(function() {
                that.create_listeners();
                that.draw(); },
            null);
        },
        set_ranges: function() {
            var x_scale = this.scales.x;
            if(x_scale) {
                x_scale.set_range(this.parent.padded_range("x", x_scale.model));
            }
            var y_scale = this.scales.y;
            if(y_scale) {
                y_scale.set_range(this.parent.padded_range("y", y_scale.model));
            }
        },
        set_positional_scales: function() {
            var x_scale = this.scales.x, y_scale = this.scales.y;
            this.listenTo(x_scale, "domain_changed", function() {
                if(!this.model.dirty) { this.draw(); }
            });
            this.listenTo(y_scale, "domain_changed", function() {
                if(!this.model.dirty) { this.draw(); }
            });
        },
        create_listeners: function() {
            OHLC.__super__.create_listeners.apply(this);
             this.el.on("mouseover", _.bind(this.mouse_over, this))
                .on("mousemove", _.bind(this.mouse_move, this))
                .on("mouseout", _.bind(this.mouse_out, this));

            this.listenTo(this.model, "change:stroke", this.update_stroke, this);
            this.listenTo(this.model, "change:stroke_width", this.update_stroke_width, this);
            this.listenTo(this.model, "change:colors", this.update_colors, this);
            this.listenTo(this.model, "change:opacities", this.update_opacities, this);
            this.listenTo(this.model, "change:marker", this.update_marker, this);
            this.listenTo(this.model, "format_updated", this.draw, this);
            this.listenTo(this.model, "data_updated", this.draw);
        },
        update_stroke: function() {
            var stroke = this.model.get("stroke");
            this.el.selectAll(".stick").style("stroke", stroke);

            if(this.legend_el) {
                this.legend_el.selectAll("path").style("stroke", stroke);
                this.legend_el.selectAll("text").style("fill", stroke);
            }
        },
        update_stroke_width: function() {
            var stroke_width = this.model.get("stroke_width");
            this.el.selectAll(".stick").attr("stroke-width", stroke_width);
        },
        update_colors: function() {
            var that = this;
            var colors = this.model.get("colors");
            var up_color = (colors[0] ? colors[0] : "none");
            var down_color = (colors[1] ? colors[1] : "none");

            // Fill candles based on the opening and closing values
            this.el.selectAll(".stick").style("fill", function(d) {
                return (d.y[that.model.px.o] > d.y[that.model.px.c] ?
                    down_color : up_color);
            });

            if(this.legend_el) {
                this.legend_el.selectAll("path").style("fill", up_color);
            }
        },
        update_opacities: function() {
            var opacities = this.model.get("opacities");
            this.el.selectAll(".stick").style("opacity", function(d, i) {
                                                    return opacities[i];
                                             });

            if(this.legend_el) {
                this.legend_el.selectAll("path")
                    .attr("opacity", function(d, i) { return opacities[i]; });
            }
        },
        update_marker: function() {
            var marker = this.model.get("marker");

            if(this.legend_el && this.rect_dim) {
                this.draw_legend_icon(this.rect_dim, this.legend_el);
            }

            // Redraw existing marks
            this.draw_mark_paths(marker, this.el,
                this.model.mark_data.map(function(d, index) {
                    return d[1];
                }));
        },
        update_selected_colors: function(idx_start, idx_end) {
            var stick_sel = this.el.selectAll(".stick");
            var current_range = _.range(idx_start, idx_end + 1);
            if(current_range.length == this.model.mark_data.length) {
                current_range = [];
            }
            var that = this;
            var stroke = this.model.get("stroke");
            var colors = this.model.get("colors");
            var up_color = (colors[0] ? colors[0] : stroke);
            var down_color = (colors[1] ? colors[1] : stroke);
            var px = this.model.px;

            _.range(0, this.model.mark_data.length)
             .forEach(function(d) {
                 that.el.selectAll("#stick" + d)
                   .style("stroke", stroke);
             });

            current_range.forEach(function(d) {
                that.el.selectAll("#stick" + d)
                    .style("stroke", function(d) {
                        return d[px.o] > d[px.c] ? down_color : up_color;
                    });
            });
        },
        invert_range: function(start_pxl, end_pxl) {
            if(start_pxl === undefined || end_pxl === undefined ||
               this.model.mark_data.length === 0)
            {
                this.update_selected_colors(-1,-1);
                selected = [];
                return selected;
            }

            var indices = _.range(this.model.mark_data.length);
            var that = this;
            var selected = _.filter(indices, function(index) {
                var elem = that.x_pixels[index];
                return (elem >= start_pxl && elem <= end_pxl);
            });

            var x_scale = this.scales.x;
            var idx_start = -1;
            var idx_end = -1;
            if(selected.length > 0 &&
                (start_pxl !== x_scale.scale.range()[0] ||
                    end_pxl !== x_scale.scale.range()[1]))
            {
                idx_start = selected[0];
                idx_end = selected[selected.length - 1];
            }
            this.update_selected_colors(idx_start, idx_end);
            this.model.set("selected", selected);
            this.touch();
            return selected;
        },
        invert_point: function(pixel) {
            var x_scale = this.scales.x;
            var point = 0;
            var abs_diff = this.x_pixels.map(function(elem) { return Math.abs(elem - pixel); });
            var sel_index = abs_diff.indexOf(d3.min(abs_diff));
            this.update_selected_colors(sel_index, sel_index);
            this.model.set("selected", [sel_index]);
            this.touch();
            return sel_index;
        },
        draw: function() {
            var x_scale = this.scales.x, y_scale = this.scales.y;
            this.set_ranges();
            var colors = this.model.get("colors");
            var opacities = this.model.get("opacities");
            var up_color = (colors[0] ? colors[0] : "none");
            var down_color = (colors[1] ? colors[1] : "none");
            var px = this.model.px;
            var stick = this.el.selectAll(".stick")
                .data(this.model.mark_data.map(function(data, index) {
                    return {'x': data[0], 'y': data[1], 'index': index};
                }));

            // Create new
            var new_sticks = stick.enter()
                .append("g")
                .attr("class", "stick")
                .attr("id", function(d, i) { return "stick"+i; })
                .style("stroke", this.model.get("stroke"))
                .style("opacity", function(d, i) {
                            return opacities[i];
                      });

            new_sticks.append("path").attr("class", "stick_head");
            new_sticks.append("path").attr("class", "stick_tail");
            new_sticks.append("path").attr("class", "stick_body");

            stick.exit().remove();

            var that = this;

            // Determine offset to use for translation
            var y_index  = px.h;
            if(px.h === -1) {
                y_index = px.o;
            }
            // Update all of the marks
            this.el.selectAll(".stick")
                .style("fill", function(d, i) {
                    return (d.y[px.o] > d.y[px.c]) ? down_color : up_color;
                })
                .attr("stroke-width", this.model.get("stroke_width"));
            if(x_scale.model.type === "ordinal") {
                // If we are out of range, we just set the mark in the final
                // bucket's range band. FIXME?
                var x_max = d3.max(this.parent.range("x"));
                this.el.selectAll(".stick").attr( "transform", function(d, i) {
                    return "translate(" + ((x_scale.scale(that.model.mark_data[i][0]) !== undefined ?
                                            x_scale.scale(that.model.mark_data[i][0]) : x_max) +
                                            x_scale.scale.rangeBand()/2) + "," +
                                          (y_scale.scale(d.y[y_index]) + y_scale.offset) + ")";
                });
            } else {
                this.el.selectAll(".stick").attr( "transform", function(d, i) {
                     return "translate(" + (x_scale.scale(that.model.mark_data[i][0]) +
                                         x_scale.offset) + "," +
                                         (y_scale.scale(d.y[y_index]) +
                                         y_scale.offset) + ")";
                 });
            }

            // Draw the mark paths
            this.draw_mark_paths(this.model.get("marker"), this.el,
                this.model.mark_data.map(function(d) {
                    return d[1];
                }));

            this.x_pixels = this.model.mark_data.map(function(el) { return x_scale.scale(el[0]) + x_scale.offset; });
        },
        draw_mark_paths: function(type, selector, dat) {
            /* Calculate some values so that we can draw the marks
             *      | <----- high (0,0)
             *      |
             *  --------- <- headline_top (open or close)
             *  |       |
             *  |       |
             *  |       |
             *  --------- <- headline_bottom (open or close)
             *      |
             *      | <----- low
             *
             *
             *      | <----- high (0,0)
             *  ____| <----- open
             *      |
             *      |
             *      |
             *      |____ <- close
             *      | <----- low
             */

            var px = this.model.px;
            var that = this;
            var open = [];
            var high = [];
            var low = [];
            var close = [];
            var headline_top = [];
            var headline_bottom = [];
            var to_left_side = [];
            var scaled_mark_widths = [];

            var min_x_difference = this.calculate_mark_width();
            var x_scale = this.scales.x, y_scale = this.scales.y;
            var offset_in_x_units, data_point;

            for(var i = 0; i < dat.length; i++) {
                if(px.o === -1) {
                    open[i] = undefined;
                } else {
                    open[i] = y_scale.scale(dat[i][px.o]);
                }
                if(px.c === -1) {
                    close[i] = undefined;
                } else {
                    close[i] = y_scale.scale(dat[i][px.c]);
                }
                // We can only compute these (and only need to compute these)
                // when we have both the open and the close values
                if(px.o !== -1 && px.c !== -1) {
                    headline_top[i] = (dat[i][px.o] > dat[i][px.c]) ?
                                            open[i] : close[i];
                    headline_bottom[i] = (dat[i][px.o] < dat[i][px.c]) ?
                                            open[i] : close[i];
                }

                // We never have high without low and vice versa, so we can
                // check everything at once
                if(px.h === -1 || px.l === -1) {
                    high[i] = open[i];
                    low[i] = close[i];
                } else {
                    high[i] = y_scale.scale(dat[i][px.h]);
                    low[i] = y_scale.scale(dat[i][px.l]);
                }

                data_point = that.model.mark_data[i][0];
                // Check for dates so that we don't concatenate
                if( min_x_difference instanceof Date) {
                    min_x_difference = min_x_difference.getTime();
                }
                if(data_point instanceof Date) {
                    data_point = data_point.getTime();
                }
                offset_in_x_units = data_point + min_x_difference;

                if(x_scale.model.type === "ordinal") {
                    scaled_mark_widths[i] = x_scale.scale.rangeBand() * 0.75;
                } else {
                    scaled_mark_widths[i] = (x_scale.scale(offset_in_x_units) -
                                             x_scale.scale(data_point)) *
                                             0.75;
                }
                to_left_side[i] = -1*scaled_mark_widths[i]/2;
            }

            // Determine OHLC marker type
            // Note: if we do not have open or close data then we have to draw
            // a bar.
            if(type == "candle" && px.o !== -1 && px.c !== -1) {
                /*
                 *      | <-------- head
                 *  ---------
                 *  |       |
                 *  |       | <---- body
                 *  |       |
                 *  ---------
                 *      | <-------- tail
                 */
                if(px.h !== -1 || px.l !== -1) {
                    selector.selectAll(".stick_head")
                        .attr("d", function(d, i) {
                            return that.head_path_candle(headline_top[i] - high[i]);
                        });
                    selector.selectAll(".stick_tail")
                        .attr("d", function(d, i) {
                            return that.tail_path_candle(headline_bottom[i] - high[i],
                                                         low[i] - headline_bottom[i]);
                        });
                } else {
                    selector.selectAll(".stick_head").attr("d", "");
                    selector.selectAll(".stick_tail").attr("d", "");
                }
                selector.selectAll(".stick_body")
                    .attr("d", function(d, i) {
                        return that.body_path_candle(to_left_side[i],
                                                     open[i] - high[i],
                                                     scaled_mark_widths[i],
                                                     close[i] - open[i]);
                  });
            } else {
                // bar
                /*
                 *      |
                 *  ____| <-------- head (horizontal piece)
                 *      |
                 *      | <-------- body (vertical piece)
                 *      |
                 *      |____ <---- tail (horizontal piece)
                 *      |
                 */
                if(px.o !== -1) {
                    selector.selectAll(".stick_head")
                        .attr("d", function(d, i) {
                            return that.head_path_bar(to_left_side[i],
                                                      open[i] - high[i],
                                                      to_left_side[i]*-1);
                        });
                } else {
                    selector.selectAll(".stick_head").attr("d", "");
                }
                if(px.c !== -1) {
                    selector.selectAll(".stick_tail")
                        .attr("d", function(d, i) {
                            return that.tail_path_bar(close[i] - high[i],
                                                      to_left_side[i]*-1);
                        });
                } else {
                    selector.selectAll(".stick_tail").attr("d", "");
                }
                selector.selectAll(".stick_body")
                    .attr("d", function(d, i) {
                        return that.body_path_bar(low[i]-high[i]);
                    });
            }
        },
        /* SVG path for head of candle */
        head_path_candle: function(height) {
            return "m0,0 l0," + height;
        },
        /* SVG path for tail of candle */
        tail_path_candle: function(y_offset, height) {
            return "m0," + y_offset + " l0," + height;
        },
        /* SVG path for body of candle */
        body_path_candle: function(x_offset, y_offset, width, height) {
            return "m" + x_offset + "," + y_offset + " l" + width + ",0" +
                " l0," + height + " l" + (-1*width) + ",0" + " z";
        },
        /* SVG path for head of bar */
        head_path_bar: function(x_offset, y_offset, width) {
            return "m" + x_offset + "," + y_offset +
                  " l" + width + ",0";
        },
        /* SVG path for tail of bar */
        tail_path_bar: function(y_offset, width) {
            return "m0," + y_offset +
                    " l" + width + ",0";
        },
        /* SVG path for body of bar */
        body_path_bar: function(height) {
            return "m0,0 l0," + height;
        },
        calculate_mark_width: function() {
            /*
             * Calculate the mark width for this data set based on the minimum
             * distance between consecutive points.
             */
            var that = this;
            var min_distance = Number.POSITIVE_INFINITY;
            var sum = 0;
            var average_height = 0;
            var scales = this.model.get("scales");
            var x_scale = scales.x;

            for(var i = 1; i < that.model.mark_data.length; i++) {
                var dist = that.model.mark_data[i][0] -
                           that.model.mark_data[i-1][0];
                if(dist < min_distance) min_distance = dist;
            }
            // Check if there are less than two data points
            if(min_distance === Number.POSITIVE_INFINITY) {
                min_distance = (x_scale.domain[1] -
                                x_scale.domain[0]) / 2;
            }
            if(min_distance < 0) {
                min_distance = -1 * min_distance;
            }
            return min_distance;
        },
        relayout: function() {
            OHLC.__super__.relayout.apply(this);
            this.set_ranges();
            this.el.select(".intselmouse")
                .attr("width", this.width)
                .attr("height", this.height);

            // We have to redraw every time that we relayout
            this.draw();
        },
        draw_legend: function(elem, x_disp, y_disp, inter_x_disp, inter_y_disp) {
            var stroke = this.model.get("stroke");
            var colors = this.model.get("colors");
            var up_color = (colors[0] ? colors[0] : "none");
            var down_color = (colors[1] ? colors[1] : "none");
            this.rect_dim = inter_y_disp * 0.8;
            var that = this;

            this.legend_el  = elem.selectAll("#legend" + this.uuid)
                                  .data([this.model.mark_data]);

            var leg = this.legend_el.enter().append("g")
                .attr("transform", function(d, i) {
                    return "translate(0, " + (i * inter_y_disp + y_disp) + ")";
                })
                .attr("class", "legend")
                .attr("id", "legend" + this.uuid)
                .style("fill", up_color)
                .on("mouseover", _.bind(this.highlight_axes, this))
                .on("mouseout", _.bind(this.unhighlight_axes, this));

            leg.append("path").attr("class", "stick_head stick");
            leg.append("path").attr("class", "stick_tail stick");
            leg.append("path").attr("class", "stick_body stick")
                              .style("fill", up_color);

            // Add stroke color and set position
            leg.selectAll("path")
                .style("stroke", stroke)
                .attr("transform", "translate(" + (that.rect_dim/2) + ",0)");

            // Draw icon and text
            this.draw_legend_icon(that.rect_dim, leg);
            this.legend_el.append("text")
                .attr("class", "legendtext sticktext")
                .attr("x", that.rect_dim * 1.2)
                .attr("y", that.rect_dim / 2)
                .attr("dy", "0.35em")
                .text(function(d, i) { return that.model.get("labels")[i]; })
                .style("fill", stroke);

            var max_length = d3.max(this.model.get("labels"), function(d) {
                return d.length;
            });

            this.legend_el.exit().remove();
            return [1, max_length];
        },
        draw_legend_icon: function(size, selector) {
            /*
             * Draw OHLC icon next to legend text
             * Drawing the icon like this means we can avoid scaling when we
             * already know what the size of the mark is in pixels
             */
            var height = size;
            var width = size / 2;
            var bottom_y_offset = size * 3 / 4;
            var top_y_offset = size / 4;
            if(this.model.get("marker") === "candle") {
                selector.selectAll(".stick_head").attr("d",
                    this.head_path_candle(width/2));
                selector.selectAll(".stick_tail").attr("d",
                    this.tail_path_candle(bottom_y_offset, width/2));
                selector.selectAll(".stick_body").attr("d",
                    this.body_path_candle(width*-1/2, top_y_offset, width,
                                          height/2));
            } else { // bar
                selector.selectAll(".stick_head").attr("d",
                    this.head_path_bar(width*-1/2, bottom_y_offset, width/2));
                selector.selectAll(".stick_tail").attr("d",
                    this.tail_path_bar(top_y_offset, width/2));
                selector.selectAll(".stick_body").attr("d",
                    this.body_path_bar(height));
            }
        },
    });

    return {
        OHLC: OHLC,
    };
});

