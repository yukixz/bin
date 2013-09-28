if (typeof String.prototype.startsWith != 'function') {
  String.prototype.startsWith = function (str){
    return this.slice(0, str.length) == str;
  };
}
if (typeof String.prototype.contains != 'function') {
  String.prototype.contains = function (str){
    return this.indexOf(str) != -1;
  };
}