export class Distance {
  startId: number;
  endId: number;
  distance: number;

  constructor(startId: number, endId: number, distance: number) {
    this.startId = startId;
    this.endId = endId;
    this.distance = distance;
  }

  public to_string(): string {
    return "" + this.startId + ", " + this.endId + ", " + this.distance + " pas.";
  }
}
