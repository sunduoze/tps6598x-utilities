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

define(["./components/d3/d3", "./Mark", "./utils"], function(d3, MarkViewModule, utils) {
    "use strict";

    var Bars = MarkViewModule.Mark.extend({
        render: function() {
            this.padding = this.model.get("padding");
            var base_creation_promise = Bars.__super__.render.apply(this);
            this.set_internal_scales();
            this.selected_indices = this.model.get("selected");
            this.selected_style = this.model.get("selected_style");
            this.unselected_style = this.model.get("unselected_style");

            this.display_el_classes = ["bar", "legendtext"];

            var that = this;
            this.displayed.then(function() {
                that.parent.tooltip_div.node().appendChild(that.tooltip_div.node());
                that.create_tooltip();
            });

            return base_creation_promise.then(function() {
                that.event_listeners = {};
                that.process_interactions();
                that.create_listeners();
                that.compute_view_padding();
                that.draw();
            });
        },
        set_ranges: function() {
            var x_scale = this.scales.x,
                y_scale = this.scales.y;
            if(x_scale.model.type !== "ordinal") {
                x_scale.set_range(this.parent.padded_range("x", x_scale.model));
            } else {
                x_scale.set_range(this.parent.padded_range("x", x_scale.model), this.padding);
            }
            y_scale.set_range(this.parent.padded_range("y", y_scale.model));
            // x_offset is set later by the adjust_offset method
            // This differs because it is not constant for a scale.
            // Changes based on the data.
            this.x_offset = 0;
            this.y_offset = y_scale.offset;
        },
        set_positional_scales: function() {
            var x_scale = this.scales.x, y_scale = this.scales.y;
            this.listenTo(x_scale, "domain_changed", function() {
                if (!this.model.dirty) {
                    this.draw();
                }
            });
            this.listenTo(y_scale, "domain_changed", function() {
                if (!this.model.dirty) {
                    this.draw();
                }
            });
        },
        set_internal_scales: function() {
            // Two scales to draw the bars.
            this.x = d3.scale.ordinal();
            this.x1 = d3.scale.ordinal();
        },
        adjust_offset: function() {
            // In the case of a linear scale, and when plotting ordinal data,
            // the value have to be negatively offset by half of the width of
            // the bars, because ordinal scales give the values corresponding
            // to the start of the bin but linear scale gives the actual value.
            var x_scale = this.scales.x;
            if(x_scale.model.type !== "ordinal") {
                if (this.model.get("align")==="center") {
                    this.x_offset = -(this.x.rangeBand() / 2).toFixed(2);
                } else if (this.model.get("align") === "left") {
                    this.x_offset = -(this.x.rangeBand()).toFixed(2);
                } else {
                    this.x_offset = 0;
                }
            } else {
                if (this.model.get("align")==="center") {
                    this.x_offset = 0;
                } else if (this.model.get("align")==="left") {
                    this.x_offset = -(this.x.rangeBand() / 2);
                } else {
                    this.x_offset = (this.x.rangeBand() / 2);
                }
            }
        },
        create_listeners: function() {
            Bars.__super__.create_listeners.apply(this);
            this.el
              .on("mouseover", _.bind(function() {
                  this.event_dispatcher("mouse_over");
              }, this))
              .on("mousemove", _.bind(function() {
                  this.event_dispatcher("mouse_move");
              }, this))
              .on("mouseout", _.bind(function() {
                  this.event_dispatcher("mouse_out");
              }, this));

            this.listenTo(this.model, "data_updated", function() {
                //animate bars on data update
                var animate = true;
                this.draw(animate);
            }, this);
            this.listenTo(this.model, "change:colors", this.update_colors, this);
            this.listenTo(this.model, "colors_updated", this.update_colors, this);
            this.listenTo(this.model, "change:type", this.update_type, this);
            this.listenTo(this.model, "change:align", this.realign, this);
            this.listenTo(this.model, "change:tooltip", this.create_tooltip, this);
            this.model.on_some_change(["stroke", "opacities"], this.update_stroke_and_opacities, this);
            this.listenTo(this.model, "change:selected", this.update_selected);
            this.listenTo(this.model, "change:interactions", this.process_interactions);
            this.listenTo(this.parent, "bg_clicked", function() {
                this.event_dispatcher("parent_clicked");
            });
        },
        process_interactions: function() {
            var interactions = this.model.get("interactions");
            if(_.isEmpty(interactions)) {
                //set all the event listeners to blank functions
                this.reset_interactions();
            }
            else {
                if(interactions.click !== undefined &&
                  interactions.click !== null) {
                    if(interactions.click === "tooltip") {
                        this.event_listeners.element_clicked = function() {
                            return this.refresh_tooltip(true);
                        };
                        this.event_listeners.parent_clicked = this.hide_tooltip;
                    } else if (interactions.click === "select") {
                        this.event_listeners.parent_clicked = this.reset_selection;
                        this.event_listeners.element_clicked = this.bar_click_handler;
                    }
                } else {
                    this.reset_click();
                }
                if(interactions.hover !== undefined &&
                  interactions.hover !== null) {
                    if(interactions.hover === "tooltip") {
                        this.event_listeners.mouse_over = this.refresh_tooltip;
                        this.event_listeners.mouse_move = this.show_tooltip;
                        this.event_listeners.mouse_out = this.hide_tooltip;
                    }
                } else {
                    this.reset_hover();
                }
                if(interactions.legend_click !== undefined &&
                  interactions.legend_click !== null) {
                    if(interactions.legend_click === "tooltip") {
                        this.event_listeners.legend_clicked = function() {
                            return this.refresh_tooltip(true);
                        };
                        this.event_listeners.parent_clicked = this.hide_tooltip;
                    }
                } else {
                    this.event_listeners.legend_clicked = function() {};
                }
                if(interactions.legend_hover !== undefined &&
                  interactions.legend_hover !== null) {
                    if(interactions.legend_hover === "highlight_axes") {
                        this.event_listeners.legend_mouse_over = _.bind(this.highlight_axes, this);
                        this.event_listeners.legend_mouse_out = _.bind(this.unhighlight_axes, this);
                    }
                } else {
                    this.reset_legend_hover();
                }
            }
        },
        realign: function() {
            //TODO: Relayout is an expensive call on realigning. Need to change
            //this.
            this.relayout();
        },
        relayout: function() {
            var y_scale = this.scales.y;
            this.set_ranges();
            this.compute_view_padding();

            this.el.select(".zeroLine")
              .attr("x1",  0)
              .attr("x2", this.parent.plotarea_width)
              .attr("y1", y_scale.scale(this.model.base_value))
              .attr("y2", y_scale.scale(this.model.base_value));

            this.x.rangeRoundBands(this.set_x_range(), this.padding);
            this.adjust_offset();
            this.x1.rangeRoundBands([0, this.x.rangeBand().toFixed(2)]);
            this.draw_bars();
        },
        invert_point: function(pixel) {
            if(pixel === undefined) {
                this.model.set("selected", null);
                this.touch();
                return;
            }

            var x_scale = this.scales.x;
            var abs_diff = this.x_pixels.map(function(elem) { return Math.abs(elem - pixel); });
            this.model.set("selected", [abs_diff.indexOf(d3.min(abs_diff))]);
            this.touch();
        },
        invert_range: function(start_pxl, end_pxl) {
            if(start_pxl === undefined || end_pxl === undefined) {
                this.model.set("selected", null);
                this.touch();
                return [];
            }

            var self = this;
            var x_scale = this.scales.x;

            var indices = _.range(this.model.mark_data.length);
            var filtered_indices = indices.filter(function(ind) { var x_pix = self.x_pixels[ind];
                                                                  return (x_pix <= end_pxl && x_pix >= start_pxl); });
            this.model.set("selected", filtered_indices);
            this.touch();
        },
        update_selected: function(model, value) {
            this.selected_indices = value;
            this.apply_styles();
        },
        draw: function(animate) {
            this.set_ranges();
            var colors = this.model.get("colors");
            var that = this;
            var bar_groups = this.el.selectAll(".bargroup")
              .data(this.model.mark_data, function(d) {
                  return d.key;
              });

            var x_scale = this.scales.x, y_scale = this.scales.y;
            // this.x is the ordinal scale used to draw the bars. If a linear
            // scale is given, then the ordinal scale is created from the
            // linear scale.
            if(x_scale.model.type !== "ordinal") {
                var model_domain = this.model.mark_data.map(function(elem) {
                    return elem.key;
                });
                this.x.domain(model_domain);
            } else {
                this.x.domain(x_scale.scale.domain());
            }
            this.x.rangeRoundBands(this.set_x_range(), this.padding);
            this.adjust_offset();
            this.x1.rangeRoundBands([0, this.x.rangeBand().toFixed(2)]);

            if(this.model.mark_data.length > 0) {
                this.x1.domain(_.range(this.model.mark_data[0].values.length))
                    .rangeRoundBands([0, this.x.rangeBand().toFixed(2)]);
            }
            bar_groups.enter()
              .append("g")
              .attr("class", "bargroup");
            // The below function sorts the DOM elements so that the order of
            // the DOM elements matches the order of the data they are bound
            // to. This is required to maintain integrity with selection.
            bar_groups.order();

            bar_groups.on("click", function(d, i) {
                return that.event_dispatcher("element_clicked",
                                             {"data": d, "index": i});
            });
            bar_groups.exit().remove();

            var bars_sel = bar_groups.selectAll(".bar")
              .data(function(d) {
                  return d.values;
              });

            // default values for width and height are to ensure smooth
            // transitions
            bars_sel.enter()
              .append("rect")
              .attr("class", "bar")
              .attr("width", 0)
              .attr("height", 0);

            this.draw_bars(animate);

            this.apply_styles();

            this.el.selectAll(".zeroLine").remove();
            this.el.append("g")
              .append("line")
              .attr("class", "zeroLine")
              .attr("x1",  0)
              .attr("x2", this.parent.plotarea_width)
              .attr("y1", y_scale.scale(this.model.base_value))
              .attr("y2", y_scale.scale(this.model.base_value));
        },
        draw_bars: function(animate) {
            var bar_groups = this.el.selectAll(".bargroup");
            var bars_sel = bar_groups.selectAll(".bar");
            var animation_duration = animate === true ? this.parent.model.get("animation_duration") : 0;
            var that = this;

            var x_scale = this.scales.x, y_scale = this.scales.y;
            if (x_scale.model.type === "ordinal") {
                var x_max = d3.max(this.parent.range("x"));
                bar_groups.attr("transform", function(d) {
                    return "translate(" + ((x_scale.scale(d.key) !== undefined ?
                                            x_scale.scale(d.key) : x_max) + that.x_offset) + ", 0)";
                });
            } else {
                bar_groups.attr("transform", function(d) {
                    return "translate(" + (x_scale.scale(d.key) + that.x_offset) + ", 0)";
                });
            }
            if (this.model.get("type") === "stacked") {
                bars_sel.transition().duration(animation_duration)
                    .attr("x", 0)
                    .attr("width", this.x.rangeBand().toFixed(2))
                    .attr("y", function(d) {
                        return y_scale.scale(d.y1);
                    }).attr("height", function(d) {
                        return Math.abs(y_scale.scale(d.y1 + d.y) - y_scale.scale(d.y1));
                    });
            } else {
                bars_sel.transition().duration(animation_duration)
                  .attr("x", function(datum, index) {
                        return that.x1(index);
                  }).attr("width", this.x1.rangeBand().toFixed(2))
                  .attr("y", function(d) {
                      return d3.min([y_scale.scale(d.y), y_scale.scale(that.model.base_value)]);
                  }).attr("height", function(d) {
                      return Math.abs(y_scale.scale(that.model.base_value) - (y_scale.scale(d.y)));
                  });
            }

            this.x_pixels = this.model.mark_data.map(function(el) {
                                                        return x_scale.scale(el.key) + x_scale.offset; });
        },
        update_type: function(model, value) {
            // We need to update domains here as the y_domain needs to be
            // changed when we switch from stacked to grouped.
            this.model.update_domains();
            this.draw();
        },
        update_stroke_and_opacities: function() {
            var stroke = this.model.get("stroke");
            var opacities = this.model.get("opacities");
            this.el.selectAll(".bar")
                .style("stroke", stroke)
                .style("opacity", function(d, i) {
                            return opacities[i];
                      });
        },
        update_colors: function() {
            //the following if condition is to handle the case of single
            //dimensional data.
            //if y is 1-d, each bar should be of 1 color.
            //if y is multi-dimensional, the correspoding values should be of
            //the same color.
            var that = this;
            var color_scale = this.scales.color;
            if(this.model.mark_data.length > 0) {
                if(!(this.model.is_y_2d)) {
                    this.el.selectAll(".bar").style("fill", function(d, i) {
                        return (d.color !== undefined && color_scale !== undefined) ?
                            color_scale.scale(d.color) : that.get_colors(d.color_index);
                    });
                } else {
                    this.el.selectAll(".bargroup")
                       .selectAll(".bar")
                       .style("fill", function(d, i) {
                       return (d.color !== undefined && color_scale !== undefined) ?
                           color_scale.scale(d.color) : that.get_colors(d.color_index);
                    });
                }
            }
            //legend color update
            if(this.legend_el) {
                this.legend_el.selectAll(".legendrect")
                  .style("fill", function(d, i) {
                      return (d.color && color_scale) ?
                          color_scale.scale(d.color) : that.get_colors(d.color_index);
                  });
                this.legend_el.selectAll(".legendtext")
                    .style("fill", function(d, i) {
                    return (d.color !== undefined && color_scale !== undefined) ?
                        color_scale.scale(d.color) : that.get_colors(d.color_index);
                });
            }
        },
        draw_legend: function(elem, x_disp, y_disp, inter_x_disp, inter_y_disp) {
            if(!(this.model.is_y_2d) &&
               (this.model.get("colors").length !== 1 &&
                this.model.get("color_mode") !== "element")) {
                return [0, 0];
            }

            var legend_data = this.model.mark_data[0].values.map(function(data) {
                return {
                    index: data.sub_index,
                    color: data.color,
                    color_index: data.color_index
                };
            });
            var color_scale = this.scales.color;
            this.legend_el = elem.selectAll(".legend" + this.uuid)
                .data(legend_data);

            var that = this;
            var rect_dim = inter_y_disp * 0.8;
            this.legend_el.enter()
              .append("g")
                .attr("class", "legend" + this.uuid)
                .attr("transform", function(d, i) {
                    return "translate(0, " + (i * inter_y_disp + y_disp)  + ")";
                })
                .on("mouseover", _.bind(function() {
                    this.event_dispatcher("legend_mouse_over");
                }, this))
                .on("mouseout", _.bind(function() {
                    this.event_dispatcher("legend_mouse_out");
                }, this))
                .on("click", _.bind(function() {
                    this.event_dispatcher("legend_clicked");
                }, this))
              .append("rect")
                .classed("legendrect", true)
                .style("fill", function(d,i) {
                    return (d.color !== undefined && color_scale !== undefined) ?
                        color_scale.scale(d.color) : that.get_colors(d.color_index);
                }).attr({
                    x: 0,
                    y: 0,
                    width: rect_dim,
                    height: rect_dim,
                });

            this.legend_el.append("text")
             .attr("class","legendtext")
              .attr("x", rect_dim * 1.2)
              .attr("y", rect_dim / 2)
              .attr("dy", "0.35em")
              .text(function(d, i) { return that.model.get("labels")[i]; })
              .style("fill", function(d,i) {
                  return (d.color !== undefined && color_scale !== undefined) ?
                      color_scale.scale(d.color) : that.get_colors(d.color_index);
              });

            var max_length = d3.max(this.model.get("labels"), function(d) {
                return d.length;
            });

            this.legend_el.exit().remove();
            return [this.model.mark_data[0].values.length, max_length];
        },
        clear_style: function(style_dict, indices) {
            // Function to clear the style of a dict on some or all the elements of the
            // chart. If indices is null, clears the style on all elements. If
            // not, clears on only the elements whose indices are mathcing.
            //
            // This function is not used right now. But it can be used if we
            // decide to accomodate more properties than those set by default.
            // Because those have to cleared specifically.
            var elements = this.el.selectAll(".bargroup");
            if(indices !== undefined) {
                elements = elements.filter(function(d, index) {
                    return indices.indexOf(index) !== -1;
                });
            }
            var clearing_style = {};
            for(var key in style_dict) {
                clearing_style[key] = null;
            }
            elements.selectAll(".bar").style(clearing_style);
        },
        set_style_on_elements: function(style, indices) {
            // If the index array is undefined or of length=0, exit the
            // function without doing anything
            if(indices === undefined || indices === null || indices.length === 0) {
                return;
            }
            // Also, return if the style object itself is blank
            if(Object.keys(style).length === 0) {
                return;
            }
            var elements = this.el.selectAll(".bargroup");
            elements = elements.filter(function(data, index) {
                return indices.indexOf(index) !== -1;
            });
            elements.selectAll(".bar").style(style);
        },
        set_default_style: function(indices) {
            // For all the elements with index in the list indices, the default
            // style is applied.
            this.update_colors();
            this.update_stroke_and_opacities();
        },
        set_x_range: function() {
            var x_scale = this.scales.x;
            if(x_scale.model.type === "ordinal") {
                return x_scale.scale.rangeExtent();
            } else {
                return [x_scale.scale(d3.min(this.x.domain())),
                        x_scale.scale(d3.max(this.x.domain()))];
            }
        },
        bar_click_handler: function (args) {
            var data = args.data;
            var index = args.index;
            var that = this;
            var idx = this.model.get("selected");
            var selected = idx ? utils.deepCopy(idx) : [];
            var elem_index = selected.indexOf(index);
            // index of bar i. Checking if it is already present in the
            // list
            if(elem_index > -1 && d3.event.ctrlKey) {
                // if the index is already selected and if ctrl key is
                // pressed, remove the element from the list
                selected.splice(elem_index, 1);
            } else {
                if(d3.event.shiftKey) {
                    //If shift is pressed and the element is already
                    //selected, do not do anything
                    if(elem_index > -1) {
                        return;
                    }
                    //Add elements before or after the index of the current
                    //bar which has been clicked
                    var min_index = (selected.length !== 0) ?
                        d3.min(selected) : -1;
                    var max_index = (selected.length !== 0) ?
                        d3.max(selected) : that.model.mark_data.length;
                    if(index > max_index){
                        _.range(max_index+1, index+1).forEach(function(i) {
                            selected.push(i);
                        });
                    } else if(index < min_index){
                        _.range(index, min_index).forEach(function(i) {
                            selected.push(i);
                        });
                    }
                } else if(d3.event.ctrlKey) {
                    //If ctrl is pressed and the bar is not already selcted
                    //add the bar to the list of selected bars.
                    selected.push(index);
                }
                // updating the array containing the bar indexes selected
                // and updating the style
                else {
                    //if ctrl is not pressed, then clear the selected ones
                    //and set the current element to the selected
                    selected = [];
                    selected.push(index);
                }
            }
            this.model.set("selected",
                           ((selected.length === 0) ? null : selected),
                           {updated_view: this});
            this.touch();
            if(!d3.event) {
                d3.event = window.event;
            }
            var e = d3.event;
            if(e.cancelBubble !== undefined) { // IE
                e.cancelBubble = true;
            }
            if(e.stopPropagation) {
                e.stopPropagation();
            }
            e.preventDefault();
        },
        reset_selection: function() {
            this.model.set("selected", null);
            this.selected_indices = null;
            this.touch();
        },
        compute_view_padding: function() {
            //This function returns a dictionary with keys as the scales and
            //value as the pixel padding required for the rendering of the
            //mark.
            var x_scale = this.scales.x;
            var x_padding = 0;
            if(x_scale) {
                if (this.x !== null && this.x !== undefined &&
                    this.x.domain().length !== 0) {
                    if(x_scale.model.type === "linear") {
                        if (this.model.get("align") === "center") {
                            x_padding = (this.parent.plotarea_width / (2.0 * this.x.domain().length) + 1);
                        } else if (this.model.get("align") === "left" ||
                                   this.model.get("align") === "right") {
                            x_padding = (this.parent.plotarea_width / (this.x.domain().length) + 1);
                        }
                    } else {
                        if (this.model.get("align") === "left" ||
                            this.model.get("align") === "right") {
                            x_padding = ( this.x.rangeBand() / 2 ).toFixed(2);
                        }
                    }
                }
            }
            if(x_padding !== this.x_padding) {
                this.x_padding = x_padding;
                this.trigger("mark_padding_updated");
                //dispatch the event
            }
        },
    });

    return {
        Bars: Bars,
    };
});


