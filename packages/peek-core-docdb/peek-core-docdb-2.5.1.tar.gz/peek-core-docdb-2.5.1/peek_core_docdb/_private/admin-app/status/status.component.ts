import { Component } from "@angular/core"
import { BalloonMsgService, NgLifeCycleEvents } from "@synerty/peek-plugin-base-js"
import { TupleDataObserverService, TupleSelector } from "@synerty/vortexjs"
import { AdminStatusTuple } from "@peek/peek_core_docdb/_private"

@Component({
    selector: "pl-docdb-status",
    templateUrl: "./status.component.html"
})
export class StatusComponent extends NgLifeCycleEvents {
    
    item: AdminStatusTuple = new AdminStatusTuple()
    
    constructor(
        private balloonMsg: BalloonMsgService,
        private tupleObserver: TupleDataObserverService
    ) {
        super()
        
        let ts = new TupleSelector(AdminStatusTuple.tupleName, {})
        this.tupleObserver.subscribeToTupleSelector(ts)
            .takeUntil(this.onDestroyEvent)
            .subscribe((tuples: AdminStatusTuple[]) => {
                this.item = tuples[0]
            })
        
    }
    
}
