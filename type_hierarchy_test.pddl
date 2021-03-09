(define (domain test-adl)
    (:types
        truck
        airplane - vehicle
        package
        vehicle - physobj
        airport
        location - place
        city
        place
        physobj - object)

    (:test
        v1 - vehicle
        t2 - truck
        sachsen - location
        berlin  - city
        )

    (:action move
    :parameters (?who - agent ?from - square ?to - square)
    :precondition (and (alive ?who)
		       (at ?who ?from)
		       (adj ?from ?to)
                        )
    :effect (and (not (at ?who ?from))
		 (at ?who ?to)

		 (when (pit ?to)
		   (and (not (alive ?who))))

		 (when (exists (?w - wumpus) (and (at ?w ?to) (alive ?w)))
		   (and (not (alive ?who)))))
    )

  (:action take
    :parameters (?who - agent ?where - square ?what)
    :precondition (and (alive ?who)
		       (at ?who ?where)
		       (at ?what ?where))
    :effect (and (have ?who ?what)
		 (not (at ?what ?where)))
    )


)