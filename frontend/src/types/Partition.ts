import { Machine } from "./Machine";

export class PartitionStatus {
  total: number;
  draining: number;
  mixed: number;
  allocated: number;
  down: number;
  idle: number;
  constructor(
    total: number,
    draining: number,
    mixed: number,
    allocated: number,
    down: number,
    idle: number
  ) {
    this.total = total;
    this.draining = draining;
    this.mixed = mixed;
    this.allocated = allocated;
    this.down = down;
    this.idle = idle;
  }
}
export class Partition {
  public machinelist: Array<Machine>;
  public name: String;

  public constructor(name: String) {
    this.name = name;
    this.machinelist = new Array<Machine>();
  }
  addMachine(newMachine: Machine) {
    this.machinelist.push(newMachine);
  }
  getStatus(): PartitionStatus {}
}
