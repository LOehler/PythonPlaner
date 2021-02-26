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
        t1 - vehicle
        t2 - truck)


)