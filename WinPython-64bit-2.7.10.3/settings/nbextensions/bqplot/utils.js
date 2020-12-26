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

define(["./components/d3/d3"], function(d3) {
    "use strict";
     //the following is a regex to match all valid time formats that can be
     //generated with d3 as of 2nd March 2015. If new formats are added to d3
     //those new formats need to be added to the regex
    var time_format_regex = new RegExp("^(((((\\*)|(/*)|(-*))(\\s*)%([aAbBdeHIjmMLpSUwWyYZ]{1}))+)|((\\s*)%([cxX]{1})))$");
    return {
        getCustomRange: function(array) {
            var first = array[0];
            var end = array[array.length - 1];
            var pivot;
            if(array[0] > array[1]) {
                pivot = d3.min(array);
            } else {
                pivot = d3.max(array);
            }
            return [d3.scale.linear().range([first, pivot]), d3.scale.linear().range([pivot, end])];
        },
        deepCopy: function (obj) {
            // This makes a deep copy of JSON-parsable objects
            // (no cycling or recombining)
            // Backbone model attributes must be JSON parsable. Hence there is
            // no need for a fancier logic, and it is surprisingly efficient.
            return JSON.parse(JSON.stringify(obj));
        },
        is_valid_time_format: function(format) {
            return time_format_regex.test(format);
        },
    };
});
